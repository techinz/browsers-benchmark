(() => {
    const result = { recaptcha_score: null };

    const responsePre = document.querySelector('pre.response');
    if (!responsePre) return result;

    try {
        const responseData = JSON.parse(responsePre.textContent);
        result.recaptcha_score = typeof responseData.score === 'number' ? responseData.score : null;
    } catch (e) {
    }

    return result;
})();