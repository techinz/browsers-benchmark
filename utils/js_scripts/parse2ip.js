(() => {
    const result = { ip: null };

    const ipDiv = document.querySelector('div.ip span');
    if (!ipDiv) return result;

    result.ip = ipDiv.textContent.trim();

    return result;
})();