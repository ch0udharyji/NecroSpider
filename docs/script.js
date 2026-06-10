// Copy to Clipboard
function copyInstall() {
    const textToCopy = document.getElementById('install-cmd').innerText;
    
    navigator.clipboard.writeText(textToCopy).then(() => {
        const btn = document.querySelector(".copy-btn");
        const originalHTML = btn.innerHTML;
        
        // Show checkmark icon for success
        btn.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>`;
        btn.classList.add("success");
        
        setTimeout(() => {
            btn.innerHTML = originalHTML;
            btn.classList.remove("success");
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy text: ', err);
    });
}
