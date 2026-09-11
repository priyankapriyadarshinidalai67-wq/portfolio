const menuBtn = document.getElementById('menuBtn');
const mobilePanel = document.getElementById('mobilePanel');

menuBtn.addEventListener('click', () => {
  const isOpen = mobilePanel.classList.toggle('open');
  menuBtn.setAttribute('aria-expanded', isOpen);
});

mobilePanel.querySelectorAll('a').forEach(a => {
  a.addEventListener('click', () => {
    mobilePanel.classList.remove('open');
    menuBtn.setAttribute('aria-expanded', 'false');
  });
});

const root = document.documentElement;
const themeToggle = document.getElementById('themeToggle');
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
const contactFormWrap = document.getElementById('contactFormWrap');
const openContactFormBtn = document.getElementById('openContactForm');
const contactForm = document.getElementById('contactForm');
const contactSuccess = document.getElementById('contactSuccess');
const contactError = document.getElementById('contactError');

if (prefersDark) {
  root.setAttribute('data-theme', 'dark');
}

themeToggle.addEventListener('click', () => {
  const isDark = root.getAttribute('data-theme') === 'dark';
  root.setAttribute('data-theme', isDark ? 'light' : 'dark');
});

openContactFormBtn.addEventListener('click', () => {
  const isHidden = contactFormWrap.style.display === 'none';
  contactFormWrap.style.display = isHidden ? 'block' : 'none';
  if (isHidden) {
    contactFormWrap.scrollIntoView({ behavior: 'smooth', block: 'start' });
    contactForm.querySelector('input[name="name"]').focus();
  }
});

contactForm.addEventListener('submit', async (event) => {
  event.preventDefault();

  const formData = new FormData(contactForm);
  const payload = Object.fromEntries(formData.entries());

  contactSuccess.classList.remove('show');
  contactError.classList.remove('show');

  try {
    const response = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    const result = await response.json();

    if (!response.ok || !result.success) {
      throw new Error(result.message || 'Failed to send message.');
    }

    contactSuccess.textContent = result.message;
    contactSuccess.classList.add('show');
    contactForm.reset();
  } catch (error) {
    contactError.textContent = error.message || 'Something went wrong. Please try again.';
    contactError.classList.add('show');
  }
});

async function loadApiData() {
  const statusEl = document.getElementById('apiStatus');
  const listEl = document.getElementById('portfolioList');

  try {
    const healthResponse = await fetch('/api/health');
    const healthData = await healthResponse.json();

    statusEl.textContent = `${healthData.framework} API is online: ${healthData.message}`;

    const portfolioResponse = await fetch('/api/portfolio');
    const portfolioData = await portfolioResponse.json();

    listEl.innerHTML = portfolioData.projects.map(project => `
      <li><strong>${project.name}</strong> — ${project.description}</li>
    `).join('');
  } catch (error) {
    statusEl.textContent = 'Flask API is not available yet. Start the app server to enable it.';
    listEl.innerHTML = '<li>Check the backend server and refresh the page.</li>';
    console.error('API request failed:', error);
  }
}

if (window.React && window.ReactDOM) {
  const reactStack = document.getElementById('reactStack');

  if (reactStack) {
    const techStack = ['React', 'Flask', 'Python', 'AI & ML', 'JavaScript'];

    const root = ReactDOM.createRoot(reactStack);
    root.render(
      React.createElement(
        'div',
        { className: 'react-stack-panel' },
        React.createElement('div', { className: 'section-kicker' }, 'Tech stack'),
        React.createElement(
          'div',
          { className: 'react-stack-grid' },
          techStack.map((item) =>
            React.createElement('span', { key: item, className: 'react-chip' }, item)
          )
        )
      )
    );
  }
}

loadApiData();
