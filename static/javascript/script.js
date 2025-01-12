// Copy referral link to clipboard
// document.getElementById('copy-link-btn').addEventListener('click', () => {
//     const referralLink = document.getElementById('referral-link').textContent;
//     navigator.clipboard.writeText(referralLink).then(() => {
//         alert('Referral link copied to clipboard!');
//     }).catch(err => {
//         console.error('Failed to copy referral link:', err);
//     });
// });

// Copy Referral Code
document.getElementById('copy-code-btn').addEventListener('click', function () {
    const referralCode = document.getElementById('referral-code').innerText;
    navigator.clipboard.writeText(referralCode).then(() => {
        alert('Referral code copied to clipboard!');
    });
});

// Share on Facebook
function shareOnFacebook() {
    const referralLink = document.getElementById('referral-link').textContent;
    const url = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(referralLink)}`;
    window.open(url, '_blank');
}

// Share on Twitter
function shareOnTwitter() {
    const referralLink = document.getElementById('referral-link').textContent;
    const text = "Check out this amazing referral program!";
    const url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(referralLink)}`;
    window.open(url, '_blank');
}

// Share on WhatsApp
function shareOnWhatsApp() {
    const referralLink = document.getElementById('referral-link').textContent;
    const text = `Check out this amazing referral program: ${referralLink}`;
    const url = `https://api.whatsapp.com/send?text=${encodeURIComponent(text)}`;
    window.open(url, '_blank');
}

// Share via Email
function shareOnEmail() {
    const referralLink = document.getElementById('referral-link').textContent;
    const subject = "Join this amazing referral program!";
    const body = `Hi,\n\nI wanted to share this referral program with you. Use my referral link to join: ${referralLink}`;
    const mailto = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    window.open(mailto, '_self');
}
