async function loadPartial(selector, url, clickedEl) {
    const res = await fetch(url);
    if (!res.ok) return;
    const html = await res.text();

    const container = document.querySelector(selector);
    container.innerHTML = html;

    // If the link contains data-year → put it into the loaded content
    const year = clickedEl.dataset.year;
    if (year) {
        const yearHeading = container.querySelector('#course-year');
        yearHeading.textContent = `Year ${year} Courses`;
        let ulHtml = "";

        fetch('jsons/Y' + year + '.json')
            .then(response => response.json()) // Parse the JSON data from the response
            .then(jsonObject => {
                for (const key in jsonObject) {
                    if (jsonObject.hasOwnProperty(key)) {
                        ulHtml += `
                                <li class="nav-item">
                                    <a class="nav-link" href="course.html" data-load data-code='${key}'>${jsonObject[key]}</a>
                                </li>
                                `
                        // console.log(`${key}: ${jsonObject[key]}`);
                    }
                }

                const courseList = container.querySelector('#course-list');
                courseList.innerHTML = ulHtml;
            })
            .catch(error => console.error('Error fetching JSON:', error));
    }

    const code = clickedEl.dataset.code;
    if (code) {
        fetch('/jsons/' + code + '.json')
            .then(response => response.json()) // Parse the JSON data from the response
            .then(jsonObject => {
                // console.log(code)

                const cCode = container.querySelector('#course-code');
                cCode.innerHTML = jsonObject.code;

                const cName = container.querySelector('#course-name');
                cCode.innerHTML = jsonObject.name;

                const cDetails = container.querySelector('#course-details');
                let cDetailText = `${jsonObject.credits} credits | Year ${jsonObject.year} `;
                if (jsonObject.semester) {
                    cDetailText += 'Semester ' + jsonObject.semester;
                }
                cDetails.innerHTML = cDetailText;

                const prereqs = container.querySelector('#prereqs');
                let prereqText = ""
                for (const prereq of jsonObject.prerequisites) {
                    prereqText += `
                            <a href="course.html" data-load data-code='${prereq}'>${prereq}</a>
                        `
                }
                if (prereqText) {
                    prereqs.innerHTML = prereqText;
                } else {
                    prereqs.innerHTML = "None";
                }

                const unitCont = container.querySelector('#unit-contents');
                let unitsText = ""
                let number = 1
                for (const unit in jsonObject.units) {
                    let topicsText = ""
                    for (const topic of jsonObject.units[unit]) {
                        topicsText += `
                            <li>${topic}</li>
                        `
                    }
                    if (topicsText == "") {
                        topicsText = "No subtopics under this unit."
                    }

                    unitsText += `
                        <div class="accordion-item">
                            <h2 class="accordion-header">
                                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                                    data-bs-target="#${number}" aria-expanded="false" aria-controls="${number}">
                                    ${unit}
                                </button>
                            </h2>
                            <div id="${number}" class="accordion-collapse collapse">
                                <div class="accordion-body">
                                    ${topicsText}
                                </div>
                            </div>
                        </div>
                    `
                    number++
                }
                if (unitsText) {
                    unitCont.innerHTML = "<h4>Units</h4>" + unitsText;
                }

                const expCont = container.querySelector('#exp-contents')
                let expText = ""
                for (const exp of jsonObject.experiments) {
                    expText += `
                        <li>${exp}</li>
                    `
                }
                if (expText) {
                    expCont.innerHTML += "<h4>Experiments</h4><ol>" + expText + "</ol>"
                }

                const refCont = container.querySelector('#ref-contents')
                let refText = ""
                for (const ref of jsonObject.references) {
                    refText += `
                        <li>${ref}</li>
                    `
                }
                if (refText) {
                    refCont.innerHTML += "<h4>References</h4><ol>" + refText + "</ol>"
                }

            })
            .catch(error => console.error('Error fetching JSON:', error));
    }

    if (url.includes("chat")) {
        initChat();
    }
}

async function initChat() {
    const messagesList = document.querySelector('.messages-list');
    const messageForm = document.querySelector('.message-form');
    const messageInput = document.querySelector('.message-input');

    const courseDict = await loadCourseDict();

    messageForm.addEventListener('submit', async (event) => {
        event.preventDefault();
        const message = messageInput.value.trim();
        if (message.length === 0) {
            return;
        }

        const queryItem = document.createElement('li');
        queryItem.classList.add('message', 'sent')
        queryItem.innerHTML = `
            <div class="message-text">
                <div class="message-sender">
                    <b>You</b>
                </div>
                <div class="message-content">
                    ${message}
                </div>
            </div>`;
        messagesList.appendChild(queryItem);
        messageInput.value = '';

        const courseCode = findCourse(message, courseDict)
        let replyText = "Sorry, I could not identify the course your query pertains to. Please include the full name of the course in your query. Note that only the courses listed in this website are accessible to me."
        
        if (courseCode) {
            const res = await fetch("/jsons/" + courseCode + ".json");
            const json = await res.json();
            const context = JSON.stringify(json);

            const prompt = `
You are Syllabot, a chatbot which answers course related questions.

Given the following course details in JSON form:
${context}

Answer this question to the best of your ability: ${message}
            `;

            replyText = await queryLLM(prompt);
        }
    
        const replyItem = document.createElement('li');
        replyItem.classList.add('message', 'received');
        replyItem.innerHTML = `
            <div class="message-text">
                <div class="message-sender">
                    <b>Syllabot</b>
                </div>
                <div class="message-content">
                    <p style="white-space: pre-wrap;">${replyText}</p>
                </div>
            </div>`;
        messagesList.appendChild(replyItem);
    })
}

async function queryLLM(promptText) {
  const res = await fetch('/.netlify/functions/query-llm', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ promptText })
  });

  if (!res.ok) {
    const err = await res.json().catch(() => null);
    throw new Error(err?.error || `Request failed (${res.status})`);
  }

  const data = await res.json();
  return data.reply;
}


function findCourse(query, courseDict) {
  const q = query.toLowerCase();

  for (const code in courseDict) {
    const name = courseDict[code].toLowerCase();
    const words = name.split(/\s+/);

    // Condition 1: course code directly in query
    if (q.includes(code.toLowerCase())) {
      return code;
    }

    // Condition 2: all words from course name appear
    const allWordsMatch = words.every(w => q.includes(w));
    if (allWordsMatch) {
      return code;
    }
  }

  return null;
}

async function loadCourseDict() {
  const urls = [
    '/jsons/Y1.json',
    '/jsons/Y2.json',
    '/jsons/Y3.json',
    '/jsons/Y4.json',
  ];

  let courseDict = {};

  for (const url of urls) {
    const res = await fetch(url);
    const json = await res.json();
    courseDict = { ...courseDict, ...json };   // merge into one dict
  }

  return courseDict;
}



loadPartial('#page-content', 'home.html');

document.addEventListener('click', function (e) {
    const link = e.target.closest('a[data-load]');
    if (!link) return;

    e.preventDefault();
    const url = link.getAttribute('href');

    if (url.includes("course"))
        loadPartial('#course-content', url, link);
    else
        loadPartial('#page-content', url, link);
});
