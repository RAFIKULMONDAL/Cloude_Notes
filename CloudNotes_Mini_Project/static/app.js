(() => {
  const modal = document.getElementById("composerModal");
  const openButtons = [document.getElementById("openComposer"), document.getElementById("emptyPublish")].filter(Boolean);
  const closeButtons = [document.getElementById("closeComposer"), document.getElementById("cancelComposer")].filter(Boolean);
  const titleInput = document.getElementById("title");
  const messageInput = document.getElementById("message");
  const titleCount = document.getElementById("titleCount");
  const messageCount = document.getElementById("messageCount");
  const searchInput = document.getElementById("searchInput");
  const cards = [...document.querySelectorAll(".notice-card")];
  const tabs = [...document.querySelectorAll(".category-tab")];
  const sideFilters = [...document.querySelectorAll(".side-filter")];
  const emptyState = document.getElementById("emptyState");
  const noResults = document.getElementById("noResults");
  const sortButton = document.getElementById("sortButton");
  let selectedCategory = "All";
  let newestFirst = true;

  function openModal() {
    modal.hidden = false;
    document.body.style.overflow = "hidden";
    setTimeout(() => titleInput.focus(), 40);
  }
  function closeModal() {
    modal.hidden = true;
    document.body.style.overflow = "";
  }
  openButtons.forEach(button => button.addEventListener("click", openModal));
  closeButtons.forEach(button => button.addEventListener("click", closeModal));
  modal.addEventListener("click", event => { if (event.target === modal) closeModal(); });
  document.addEventListener("keydown", event => {
    if (event.key === "Escape" && !modal.hidden) closeModal();
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
      event.preventDefault(); searchInput.focus();
    }
  });

  function updateCount(input, output, max) {
    output.textContent = `${input.value.length} / ${max}`;
  }
  titleInput.addEventListener("input", () => updateCount(titleInput, titleCount, 100));
  messageInput.addEventListener("input", () => updateCount(messageInput, messageCount, 500));

  function chooseCategory(category) {
    selectedCategory = category;
    tabs.forEach(tab => tab.classList.toggle("selected", tab.dataset.category === category));
    sideFilters.forEach(button => button.classList.toggle("selected", button.dataset.category === category));
    applyFilters();
  }
  tabs.forEach(tab => tab.addEventListener("click", () => chooseCategory(tab.dataset.category)));
  sideFilters.forEach(button => button.addEventListener("click", () => chooseCategory(button.dataset.category)));
  searchInput.addEventListener("input", applyFilters);

  function applyFilters() {
    const term = searchInput.value.trim().toLowerCase();
    let visible = 0;
    cards.forEach(card => {
      const categoryMatch = selectedCategory === "All" || card.dataset.category === selectedCategory;
      const searchMatch = !term || card.dataset.search.includes(term);
      const show = categoryMatch && searchMatch;
      card.hidden = !show;
      if (show) visible++;
    });
    if (emptyState) emptyState.hidden = cards.length > 0;
    noResults.hidden = !(cards.length > 0 && visible === 0);
    if (emptyState && cards.length === 0) emptyState.hidden = false;
  }
  document.getElementById("clearFilters").addEventListener("click", () => {
    searchInput.value = "";
    chooseCategory("All");
  });
  sortButton.addEventListener("click", () => {
    newestFirst = !newestFirst;
    const grid = document.getElementById("noticeGrid");
    const sorted = [...cards].sort((a, b) => {
      const comparison = (a.dataset.date || "").localeCompare(b.dataset.date || "");
      return newestFirst ? -comparison : comparison;
    });
    sorted.forEach(card => grid.insertBefore(card, emptyState));
    sortButton.querySelector("span").textContent = newestFirst ? "Newest first" : "Oldest first";
    applyFilters();
  });
  // A notice is already saved by Flask before the page reloads; close modal on form submission.
  document.getElementById("noticeForm").addEventListener("submit", event => {
    if (!titleInput.value.trim() || !messageInput.value.trim()) {
      event.preventDefault();
      if (!titleInput.value.trim()) titleInput.focus(); else messageInput.focus();
    }
  });
  applyFilters();
})();
