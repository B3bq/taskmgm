Promise.all([
    fetch("locales/en_translation.json").then(res => res.json()),
    fetch("locales/pl_translation.json").then(res => res.json())
]).then(([en, pl]) => {
    const userLang = navigator.language.startsWith("en") ? "en" : "pl";

    i18next.init({
        lng: navigator.language.startsWith("en") ? "en" : "pl",
        fallbackLng: "en",
        resources: {
            en: { translation: en },
            pl: { translation: pl }
        }
    }).then(() => {
        document.querySelector("html").lang = userLang;
        translatePage();
    })
})

function translatePage() {
    document.querySelectorAll("[data-i18n]").forEach(el => {
      const key = el.getAttribute("data-i18n");
      el.innerHTML = i18next.t(key);
    });

    document.querySelectorAll("[data-i18n-attr]").forEach(el => {
        const mappings = el.getAttribute("data-i18n-attr").split(";");
        mappings.forEach(map => {
          const [attr, key] = map.split(":");
          el.setAttribute(attr.trim(), i18next.t(key.trim()));
        });
      });
}