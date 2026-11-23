const result = {
    webrtc_ip: null
};

const colSixBlocks = document.querySelectorAll('.col-six');

if (colSixBlocks.length > 5) {
    const unblurredDivs = colSixBlocks[0].querySelectorAll('.unblurred');
    for (const div of unblurredDivs) {
        const text = div.textContent.trim();
        if (text.includes('ip:')) {
            const match = text.match(/ip:\s*((?:\d{1,3}\.){3}\d{1,3})/);
            result.webrtc_ip = match ? match[1] : null;
            break;
        }
    }
}

return JSON.stringify(result); // serialize to ensure consistent output (e.g. nodriver does some weird stuff with dict objects on evaluation)
