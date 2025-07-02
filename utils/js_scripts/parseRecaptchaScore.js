(() => {
    const result = { recaptcha_score: null };

    const scoreDiv = document.querySelector('.col-md-6 big');
    if (!scoreDiv) return result;

    const match = scoreDiv.textContent.trim().match(/Your score is:\s*([\d.]+)/i);
    result.recaptcha_score = match ? parseFloat(match[1]) : null;

    return result;
})();