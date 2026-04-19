(function () {
  var burger = document.querySelector(".burger");
  var panel = document.getElementById("mobile-nav");
  if (!burger || !panel) return;

  function setOpen(open) {
    burger.setAttribute("aria-expanded", open ? "true" : "false");
    if (open) {
      panel.classList.add("is-open");
      panel.removeAttribute("hidden");
    } else {
      panel.classList.remove("is-open");
      panel.setAttribute("hidden", "");
    }
  }

  setOpen(false);

  burger.addEventListener("click", function () {
    var expanded = burger.getAttribute("aria-expanded") === "true";
    setOpen(!expanded);
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") setOpen(false);
  });

  panel.querySelectorAll("a").forEach(function (link) {
    link.addEventListener("click", function () {
      setOpen(false);
    });
  });

  window.addEventListener("resize", function () {
    if (window.matchMedia("(min-width: 900px)").matches) {
      setOpen(false);
    }
  });
})();
