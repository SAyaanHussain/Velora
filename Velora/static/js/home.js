const sections = document.querySelectorAll('.types, .travel, .major'); 
const options = {
  root: null, 
  rootMargin: '0px',
  threshold: 0.1 
};
const observer = new IntersectionObserver((entries, observer) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('zoom-in-visible');
      observer.unobserve(entry.target);
    }
  });
}, options);
sections.forEach(section => {
  section.classList.add('zoom-in');
  observer.observe(section);
});