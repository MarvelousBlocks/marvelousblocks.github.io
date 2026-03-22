document.addEventListener("DOMContentLoaded", () => {
  const cards = Array.from(document.querySelectorAll("[data-minifig]"));
  const filters = Array.from(document.querySelectorAll("[data-filter]"));
  const countAll = document.querySelector("[data-count-all]");
  const countOwned = document.querySelector("[data-count-owned]");
  const countMissing = document.querySelector("[data-count-missing]");
  const countUnknown = document.querySelector("[data-count-unknown]");

  if (!cards.length) return;

  const totals = cards.reduce(
    (acc, card) => {
      const status = card.dataset.status;
      acc.all += 1;
      if (status === "owned") acc.owned += 1;
      if (status === "missing") acc.missing += 1;
      if (status === "unknown") acc.unknown += 1;
      return acc;
    },
    { all: 0, owned: 0, missing: 0, unknown: 0 }
  );

  if (countAll) countAll.textContent = totals.all;
  if (countOwned) countOwned.textContent = totals.owned;
  if (countMissing) countMissing.textContent = totals.missing;
  if (countUnknown) countUnknown.textContent = totals.unknown;

  filters.forEach((button) => {
    button.addEventListener("click", () => {
      const selected = button.dataset.filter;
      filters.forEach((other) => other.classList.toggle("is-active", other === button));

      cards.forEach((card) => {
        const match = selected === "all" || card.dataset.status === selected;
        card.hidden = !match;
      });
    });
  });
});
