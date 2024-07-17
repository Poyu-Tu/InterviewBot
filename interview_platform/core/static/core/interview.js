async function adjustTextAreaHeight(field) {
    field.style.height = 'auto';
    field.style.height = `${field.scrollHeight}px`;
}

async function submitQuestion() {
    const input = document.getElementById('user_input');
    const messageContainer = document.getElementById('chat-container');
    const userText = input.value.trim();

    if (userText) {
        messageContainer.innerHTML += `<div>User: ${userText}</div>`;

        // 構建POST請求的表單數據
        const formData = new FormData();
        formData.append('user_input', userText);

        // 發送POST請求
        try {
            const response = await fetch('/api/interview/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                messageContainer.innerHTML += `<div>Bot: ${data.response}</div>`;
                messageContainer.scrollTop = messageContainer.scrollHeight;
                input.value = '';
                await adjustTextAreaHeight(input);
            } else {
                throw new Error('Failed to fetch');
            }
        } catch (error) {
            console.error('Error:', error);
            messageContainer.innerHTML += `<div>Error communicating with the server. Please try again later.</div>`;
        }
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

window.onload = () => {
    adjustTextAreaHeight(document.getElementById('user_input'));
}