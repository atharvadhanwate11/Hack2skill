const API_BASE = 'http://127.0.0.1:5000/api';
let currentFilter = 'full';

// DOM Elements
const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const stadiumMap = document.getElementById('stadium-map');
const notificationsList = document.getElementById('notifications-list');
const queueStatusList = document.getElementById('queue-status-list');
const navItems = document.querySelectorAll('.nav-item');

// Init
document.addEventListener('DOMContentLoaded', () => {
    updateData();
    updateNotifications();
    setInterval(updateData, 5000); 
    setInterval(updateNotifications, 10000);

    // Sidebar Navigation Click Handlers
    navItems.forEach(item => {
        item.addEventListener('click', () => {
            navItems.forEach(i => i.classList.remove('active'));
            item.classList.add('active');
            currentFilter = item.dataset.filter || 'full';
            updateData(); // Refresh map with filter
        });
    });
});

// Fetch and Update Stadium Data
async function updateData() {
    try {
        const response = await fetch(`${API_BASE}/status`);
        const data = await response.json();
        
        renderMapNodes(data.stadium);
        renderQueueStatus(data.stadium);
        updateScoreboard(data.event);
    } catch (err) {
        console.error("Failed to fetch status:", err);
    }
}

function updateScoreboard(event) {
    document.getElementById('match-score').textContent = event.score;
    document.getElementById('match-time').textContent = event.time_remaining;
}

function renderMapNodes(data) {
    // Clear dynamic nodes
    const existingNodes = stadiumMap.querySelectorAll('.map-node');
    existingNodes.forEach(n => n.remove());

    let allLocations = [];
    if (currentFilter === 'full') {
        allLocations = [...data.gates, ...data.food_stalls, ...data.washrooms, ...data.destinations];
        if (data.user) allLocations.push(data.user);
    } else if (currentFilter === 'food') {
        allLocations = data.food_stalls;
    } else if (currentFilter === 'washrooms') {
        allLocations = data.washrooms;
    } else if (currentFilter === 'gates') {
        allLocations = data.gates;
    }
    
    // Safety check: if no locations found, default to full map
    if (allLocations.length === 0 && currentFilter !== 'full') {
        console.warn("Filter resulted in empty map, fallback to full map");
        allLocations = [...data.gates, ...data.food_stalls, ...data.washrooms];
    }
    
    allLocations.forEach(loc => {
        const node = document.createElement('div');
        node.className = 'map-node';
        node.style.left = `${loc.pos[0]}%`;
        node.style.top = `${loc.pos[1]}%`;
        
        // Color based on type or crowd
        let color = 'var(--green)';
        if (loc.type === 'Self') {
            color = 'var(--primary)'; // Electric Blue
            node.style.boxShadow = '0 0 20px var(--primary)';
            node.style.zIndex = '101';
            node.innerHTML = '<div style="width:100%; height:100%; background:white; border-radius:50%; border:2px solid var(--primary);"></div>';
        } else if (loc.type === 'Personal') {
            color = '#FFD700'; // Gold for destination
            node.style.boxShadow = '0 0 15px #FFD700';
            node.style.zIndex = '100';
        } else if (loc.crowd > 40) {
            color = 'var(--yellow)';
        } else if (loc.crowd > 75) {
            color = 'var(--red)';
        }
        
        node.style.backgroundColor = color;
        node.style.color = color;
        node.title = `${loc.name}: ${loc.wait} min wait`;

        // Click a node to ask the AI about it
        node.addEventListener('click', () => {
            chatInput.value = `Tell me about ${loc.name}`;
            sendMessage();
        });
        
        stadiumMap.appendChild(node);
    });
}

function renderQueueStatus(data) {
    queueStatusList.innerHTML = '';
    const stalls = data.food_stalls;
    
    stalls.forEach(stall => {
        const div = document.createElement('div');
        div.className = 'stall-status';
        
        let waitClass = 'wait-low';
        if (stall.wait > 10) waitClass = 'wait-mid';
        if (stall.wait > 20) waitClass = 'wait-high';
        
        div.innerHTML = `
            <div style="font-size: 0.85rem;">
                <div style="font-weight: 600;">${stall.name}</div>
                <div style="font-size: 0.7rem; color: var(--text-dim);">${stall.type}</div>
            </div>
            <div class="wait-pill ${waitClass}">${stall.wait} MIN</div>
        `;
        queueStatusList.appendChild(div);
    });
}

// Fetch Notifications
async function updateNotifications() {
    try {
        const response = await fetch(`${API_BASE}/notifications`);
        const alerts = await response.json();
        
        notificationsList.innerHTML = '';
        if (alerts.length === 0) {
            notificationsList.innerHTML = '<div class="notification-item">Current flow is smooth. No alerts.</div>';
            return;
        }

        alerts.forEach(alert => {
            const div = document.createElement('div');
            div.className = `notification-item ${alert.type}`;
            div.textContent = alert.msg;
            notificationsList.appendChild(div);
        });
    } catch (err) {
        console.error("Failed to fetch alerts:", err);
    }
}

// Chat Functionality
async function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;

    // Append user message
    appendMessage(text, 'user');
    chatInput.value = '';

    // Show typing...
    const typingId = 'typing-' + Date.now();
    appendMessage('Assistant is thinking...', 'ai', typingId);

    try {
        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: text })
        });
        const data = await response.json();
        
        // Replace typing with actual response
        const typingMsg = document.getElementById(typingId);
        if (typingMsg) {
            typingMsg.textContent = data.response;
        }
    } catch (err) {
        document.getElementById(typingId).textContent = "Sorry, I can't connect to the AI right now. Please try again later.";
    }
}

function appendMessage(text, side, id = null) {
    const msg = document.createElement('div');
    msg.className = `message ${side}`;
    if (id) msg.id = id;
    msg.textContent = text;
    chatMessages.appendChild(msg);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

sendBtn.addEventListener('click', sendMessage);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});
