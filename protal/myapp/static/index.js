const navToggle = document.querySelector(".nav-toggle");
const navLinks = document.querySelector(".nav-links");

if (navToggle && navLinks) {
  navToggle.addEventListener("click", () => {
    const isOpen = navLinks.classList.toggle("is-open");
    navToggle.setAttribute("aria-expanded", String(isOpen));
  });
}

document.querySelectorAll("[data-progress]").forEach((bar) => {
  const target = bar.getAttribute("data-progress") || "0";
  window.setTimeout(() => {
    bar.style.width = `${target}%`;
  }, 150);
});

document.querySelectorAll("[data-loading-text]").forEach((button) => {
  button.addEventListener("click", () => {
    if (button.form && !button.form.checkValidity()) {
      return;
    }
    button.dataset.originalText = button.textContent;
    button.textContent = button.getAttribute("data-loading-text");
    button.style.opacity = "0.72";
  });
});

const authCard = document.querySelector("[data-auth-card]");

if (authCard) {
  const tabs = authCard.querySelectorAll("[data-auth-tab]");
  const forms = authCard.querySelectorAll("[data-auth-form]");

  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      const target = tab.getAttribute("data-auth-tab");

      tabs.forEach((item) => item.classList.toggle("is-active", item === tab));
      forms.forEach((form) => {
        form.classList.toggle("is-active", form.getAttribute("data-auth-form") === target);
      });
    });
  });
}

const resumeForm = document.querySelector("[data-resume-form]");
const resumePreview = document.querySelector("[data-resume-preview]");
const scoreText = document.querySelector("[data-resume-score]");

function escapeHtml(value) {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function fieldValue(name) {
  const field = resumeForm ? resumeForm.querySelector(`[name="${name}"]`) : null;
  return field ? field.value.trim() : "";
}

function paragraphLines(value) {
  return escapeHtml(value)
    .split("\n")
    .filter(Boolean)
    .map((line) => `<div>${line}</div>`)
    .join("");
}

function updateResumePreview() {
  if (!resumeForm || !resumePreview) {
    return;
  }

  const data = {
    full_name: fieldValue("full_name"),
    email: fieldValue("email"),
    phone: fieldValue("phone"),
    location: fieldValue("location"),
    links: fieldValue("links"),
    summary: fieldValue("summary"),
    skills: fieldValue("skills"),
    projects: fieldValue("projects"),
    experience: fieldValue("experience"),
    degree: fieldValue("degree"),
    graduation: fieldValue("graduation"),
  };

  const scoreFields = Object.values(data).filter(Boolean).length;
  const score = Math.min(100, scoreFields * 10);

  if (scoreText) {
    scoreText.textContent = `${score}%`;
  }

  if (!data.full_name && !data.email) {
    resumePreview.classList.add("empty");
    resumePreview.innerHTML = "<p>Fill in your details to preview the resume.</p>";
    return;
  }

  resumePreview.classList.remove("empty");

  const contacts = [data.email, data.phone, data.location, data.links]
    .filter(Boolean)
    .map((item) => `<span>${escapeHtml(item)}</span>`)
    .join("");

  const skills = data.skills
    ? data.skills.split(",").filter(Boolean).map((skill) => `<span>${escapeHtml(skill.trim())}</span>`).join("")
    : "";

  resumePreview.innerHTML = `
    <h3 class="preview-name">${escapeHtml(data.full_name || "Your Name")}</h3>
    <div class="preview-contact">${contacts}</div>
    <div class="preview-rule"></div>
    ${data.summary ? `<section class="preview-section"><h4>Summary</h4><p>${escapeHtml(data.summary)}</p></section>` : ""}
    ${skills ? `<section class="preview-section"><h4>Technical Skills</h4><div class="skill-tags">${skills}</div></section>` : ""}
    ${data.experience ? `<section class="preview-section"><h4>Experience</h4>${paragraphLines(data.experience)}</section>` : ""}
    ${data.projects ? `<section class="preview-section"><h4>Projects</h4>${paragraphLines(data.projects)}</section>` : ""}
    ${data.degree ? `<section class="preview-section"><h4>Education</h4><p>${escapeHtml(data.degree)}</p>${data.graduation ? `<p>${escapeHtml(data.graduation)}</p>` : ""}</section>` : ""}
  `;
}

if (resumeForm) {
  resumeForm.querySelectorAll("input, textarea").forEach((field) => {
    field.addEventListener("input", updateResumePreview);
  });
  updateResumePreview();
}
