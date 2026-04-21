// Configuration
const API_BASE = 'http://localhost:5000/api';

document.addEventListener('DOMContentLoaded', () => {
    // Only run on dashboard
    if (!document.getElementById('codeEditor')) return;

    loadUserData();

    const runBtn = document.getElementById('runBtn');
    const predictBtn = document.getElementById('predictBtn');

    if (runBtn) {
        runBtn.addEventListener('click', runCode);
    }

    if (predictBtn) {
        predictBtn.addEventListener('click', predictRole);
    }
    
    // Upgrade Mock Flow
    const buyBtns = document.querySelectorAll('.buy-btn');
    buyBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
            const plan = e.target.dataset.plan;
            upgradePlan(plan);
        });
    });
});

function loadUserData() {
    const user = JSON.parse(localStorage.getItem('user'));
    if (user) {
        const xpDisplay = document.getElementById('xpDisplay');
        const roleDisplay = document.getElementById('roleDisplay');
        const userPlan = document.getElementById('userPlan');
        
        if(xpDisplay) xpDisplay.innerText = user.xp;
        if(roleDisplay) roleDisplay.innerText = user.role;
        if(userPlan) {
            userPlan.innerText = user.plan === 'pro' ? 'PRO' : 'FREE';
            if(user.plan === 'pro') userPlan.style.color = 'var(--accent)';
        }
    }
}

async function runCode() {
    const code = document.getElementById('codeEditor').value;
    const outputConsole = document.getElementById('outputConsole');
    const token = localStorage.getItem('token');

    if (!code.trim()) return;

    outputConsole.innerHTML = '<span style="color: var(--text-muted)">Running code...</span>';

    try {
        const response = await fetch(`${API_BASE}/code/run-code`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ source_code: code, language_id: 71 }) // 71 is python
        });

        const data = await response.json();

        if (response.ok) {
            let outputHtml = '';
            if (data.error) {
                outputHtml = `<span style="color: var(--danger)">Error: ${data.error}</span>`;
            } else {
                outputHtml = `<div>Status: ${data.status}</div>`;
                outputHtml += `<div class="output">${data.output || 'No output'}</div>`;
                if(data.warning) {
                     outputHtml += `<div style="color: var(--accent); margin-top: 10px;">${data.warning}</div>`;
                }
                
                // Update local XP if accepted
                if(data.status && data.status.includes('Accepted')) {
                    const user = JSON.parse(localStorage.getItem('user'));
                    user.xp += 10;
                    localStorage.setItem('user', JSON.stringify(user));
                    loadUserData();
                    showToast('Code accepted! +10 XP');
                }
            }
            outputConsole.innerHTML = outputHtml;
        } else {
            outputConsole.innerHTML = `<span style="color: var(--danger)">Error: ${data.error || 'Execution failed'}</span>`;
        }
    } catch (err) {
        console.error(err);
        outputConsole.innerHTML = `<span style="color: var(--danger)">Server connection failed. Is the backend running?</span>`;
    }
}

async function predictRole() {
    const code = document.getElementById('codeEditor').value;
    const token = localStorage.getItem('token');

    if (!code.trim()) {
        showToast('Please write some code first!');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/code/predict-role`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ code })
        });

        const data = await response.json();

        if (response.ok) {
            // Update local user role
            const user = JSON.parse(localStorage.getItem('user'));
            user.role = data.role;
            localStorage.setItem('user', JSON.stringify(user));
            loadUserData();
            showToast(data.message);
        } else {
            alert(data.error);
        }
    } catch (err) {
        console.error(err);
    }
}

async function upgradePlan(plan) {
    const token = localStorage.getItem('token');
    
    // Simulate API Call for mock payment
    try {
        const response = await fetch(`${API_BASE}/auth/upgrade-plan`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('token', data.token);
            const user = JSON.parse(localStorage.getItem('user'));
            user.plan = 'pro';
            localStorage.setItem('user', JSON.stringify(user));
            
            showToast('Payment Successful! Upgraded to PRO.');
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 2000);
        } else {
            alert(data.error);
        }
    } catch (err) {
        console.error(err);
    }
}

function showToast(msg) {
    let toast = document.getElementById('toast');
    if (!toast) {
        toast = document.createElement('div');
        toast.id = 'toast';
        toast.className = 'toast';
        document.body.appendChild(toast);
    }
    toast.innerText = msg;
    toast.style.display = 'block';
    
    setTimeout(() => {
        toast.style.display = 'none';
    }, 3000);
}
