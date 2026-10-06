(() => {
  const feedbackTimers = new WeakMap();

  function showFeedback(button, message) {
    const previousTimer = feedbackTimers.get(button);
    if (previousTimer) window.clearTimeout(previousTimer);

    const label = button.dataset.copyLabel || "value";
    button.textContent = message;
    button.setAttribute("aria-label", `${message} ${label}`);

    feedbackTimers.set(button, window.setTimeout(() => {
      button.textContent = "Copy";
      button.setAttribute("aria-label", `Copy ${label}`);
      feedbackTimers.delete(button);
    }, 1800));
  }

  // Delegation keeps the buttons working after Material's instant navigation.
  document.addEventListener("click", async (event) => {
    if (!(event.target instanceof Element)) return;
    const button = event.target.closest(".lab-copy-button");
    if (!(button instanceof HTMLButtonElement)) return;

    const target = document.getElementById(button.dataset.copyTarget || "");
    const value = target?.textContent?.trim();
    if (!value || !navigator.clipboard?.writeText) {
      showFeedback(button, "Copy unavailable");
      return;
    }

    try {
      await navigator.clipboard.writeText(value);
      showFeedback(button, "Copied");
    } catch {
      showFeedback(button, "Copy failed");
    }
  });
})();
