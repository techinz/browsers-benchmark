const result = {
//    trust_score: null,
//    bot_score: null,
    webrtc_ip: null
};

const colSixBlocks = document.querySelectorAll('.col-six');

//// trust score
//if (colSixBlocks.length > 0) {
//    const divs = colSixBlocks[0].querySelectorAll('div');
//    for (const div of divs) {
//        if (div.textContent.trim().toLowerCase().startsWith('trust score')) {
//            const span = div.querySelector('span.unblurred');
//            if (span) {
//                const match = span.textContent.trim().match(/([\d.]+)%/);
//                result.trust_score = match ? parseFloat(match[1]) : null;
//                break;
//            }
//        }
//    }
//}
//
//// bot score
//if (colSixBlocks.length > 1) {
//    const unblurredDivs = colSixBlocks[1].querySelectorAll('.unblurred');
//    for (const div of unblurredDivs) {
//        const text = div.textContent.trim();
//        if (text.startsWith('bot:')) {
//            const match = text.match(/bot:\s*([\d.]+)/);
//            result.bot_score = match ? parseFloat(match[1]) : null;
//            break;
//        }
//    }
//}

// webrtc ip
if (colSixBlocks.length > 5) {
    const unblurredDivs = colSixBlocks[6].querySelectorAll('.unblurred');
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