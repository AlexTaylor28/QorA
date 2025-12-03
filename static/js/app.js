document.addEventListener('DOMContentLoaded', () => {
    
    // 1. CSRF Token Setup for AJAX
    const getCookie = (name) => {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || getCookie('csrftoken');

    // 2. Generic Fetch Wrapper
    const apiCall = async (url, method = 'POST', body = null) => {
        const options = {
            method: method,
            headers: {
                'X-CSRFToken': csrftoken,
                'X-Requested-With': 'XMLHttpRequest'
            }
        };
        if (body) options.body = body;
        
        try {
            const response = await fetch(url, options);
            if (!response.ok) throw new Error('Network response was not ok');
            return response;
        } catch (error) {
            console.error('API Error:', error);
        }
    };

    // 3. Handle Follow Buttons (Event Delegation)
    document.body.addEventListener('click', async (e) => {
        const btn = e.target.closest('.js-follow-btn');
        if (!btn) return;

        e.preventDefault();
        
        const action = btn.dataset.action; // 'follow' or 'unfollow'
        const url = action === 'follow' ? btn.dataset.followUrl : btn.dataset.unfollowUrl;

        // Optimistic UI Update
        btn.disabled = true;
        const originalText = btn.textContent;
        btn.textContent = '...';

        const response = await apiCall(url);
        
        if (response && response.ok) {
            // Toggle State
            if (action === 'follow') {
                btn.dataset.action = 'unfollow';
                btn.textContent = 'Unfollow';
                btn.classList.add('btn-outline');
                btn.classList.remove('btn-secondary'); // Assuming base style
            } else {
                btn.dataset.action = 'follow';
                btn.textContent = 'Follow';
                btn.classList.add('btn-secondary');
                btn.classList.remove('btn-outline');
            }
        } else {
            btn.textContent = originalText; // Revert on error
        }
        btn.disabled = false;
    });
});