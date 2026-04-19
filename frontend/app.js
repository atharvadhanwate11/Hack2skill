const API_BASE = 'http://127.0.0.1:5000/api';
let currentFilter = 'full';
let userLivePos = { x: 15, y: 65 }; 
let initialGPS = null;
let userHeading = 0; // Direction in degrees

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
    initLocationWatcher(); 
    initOrientationWatcher(); // Start Heading Tracking
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

    // Venue Selector Handler
    const venueSelector = document.getElementById('venue-selector');
    venueSelector.addEventListener('change', (e) => {
        updateVenueInfo(e.target.value);
    });
    
    // Initial venue update
    updateVenueInfo(venueSelector.value);

    initVoiceInteraction();
});

function updateVenueInfo(venueId) {
    const venueMap = {
        'olympic': { 
            name: 'Olympic Main Stadium', 
            addr: 'Queen Elizabeth Olympic Park, London', 
            iframe: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2482.355152528766!2d-0.019124483750892015!3d51.53874311728286!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x48761d418047970d%3A0x6e9f8db11c9c0b11!2sLondon%20Stadium!5e0!3m2!1sen!2suk!4v1713098522306!5m2!1sen!2suk'
        },
        'lords': { 
            name: 'Lord\'s Cricket Ground', 
            addr: 'St John\'s Wood Rd, London', 
            iframe: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2482.6865242784537!2d-0.17482812328114407!3d51.52994441052601!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x48761aeba50198c3%3A0x1b41d24c015b67af!2sLord&#39;s%20Cricket%20Ground!5e0!3m2!1sen!2suk!4v1713098656752!5m2!1sen!2suk'
        },
        'metlife': { 
            name: 'MetLife Stadium', 
            addr: '1 MetLife Stadium Dr, NJ, USA', 
            iframe: 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3020.2520863071275!2d-74.07686882343277!3d40.81363293086705!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c2f861acd5c829%3A0x7d29037cba8b1c4b!2sMetLife%20Stadium!5e0!3m2!1sen!2suk!4v1713098730948!5m2!1sen!2suk'
        }
    };

    const venue = venueMap[venueId];
    if (venue) {
        document.getElementById('venue-address').textContent = venue.addr;
        document.getElementById('gmaps-link').href = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(venue.addr)}`;
        
        // Update the Live iframe
        const iframe = document.getElementById('gmaps-iframe');
        if (iframe) iframe.src = venue.iframe;
        
        // Push a system message about venue change
        appendMessage(`Switching intelligence stream to **${venue.name}**. Calibration complete.`, 'ai');
    }
}

function initVoiceInteraction() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) return;

    const recognition = new SpeechRecognition();
    recognition.lang = 'en-US';
    recognition.interimResults = false;

    // Create voice button near chat input
    const inputArea = document.querySelector('.chat-input-area');
    const voiceBtn = document.createElement('button');
    voiceBtn.className = 'send-btn';
    voiceBtn.style.background = 'var(--secondary)';
    voiceBtn.innerHTML = '🎤';
    voiceBtn.title = 'Voice Control';
    inputArea.insertBefore(voiceBtn, chatInput);

    voiceBtn.onclick = () => {
        recognition.start();
        voiceBtn.style.opacity = '0.5';
    };

    recognition.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        chatInput.value = transcript;
        sendMessage();
        voiceBtn.style.opacity = '1';
    };

    recognition.onerror = () => {
        voiceBtn.style.opacity = '1';
    };
}

function initLocationWatcher() {
    if ("geolocation" in navigator) {
        navigator.geolocation.watchPosition((position) => {
            const { latitude, longitude } = position.coords;
            
            if (!initialGPS) {
                initialGPS = { lat: latitude, lon: longitude };
            }

            // Map GPS Delta to Stadium Grid (Rough scaling: 0.0001 deg ~= 11 meters)
            // This will move your blue dot as you walk
            const deltaLat = latitude - initialGPS.lat;
            const deltaLon = longitude - initialGPS.lon;

            userLivePos.x = 15 + (deltaLon * 100000); // Scale factor for visual movement
            userLivePos.y = 65 - (deltaLat * 100000); 

            // Keep within map bounds
            userLivePos.x = Math.max(5, Math.min(95, userLivePos.x));
            userLivePos.y = Math.max(5, Math.min(95, userLivePos.y));
            
            console.log("Live GPS sync:", userLivePos);
        }, (err) => {
            console.warn("GPS Access Denied or Unavailable. Using fixed location.");
        }, { enableHighAccuracy: true });
    }
}

function initOrientationWatcher() {
    // For iOS (requires permission for orientation)
    if (typeof DeviceOrientationEvent.requestPermission === 'function') {
        document.body.addEventListener('click', () => {
            DeviceOrientationEvent.requestPermission();
        }, { once: true });
    }

    window.addEventListener('deviceorientation', (event) => {
        if (event.webkitCompassHeading) {
            userHeading = event.webkitCompassHeading;
        } else {
            userHeading = 360 - event.alpha;
        }
        
        // Update arrow rotation immediately if dot exists
        const arrow = document.getElementById('user-arrow');
        if (arrow) {
            arrow.style.transform = `translate(-50%, -100%) rotate(${userHeading}deg)`;
        }
    }, true);
}

// Fetch and Update Stadium Data
async function updateData() {
    try {
        const response = await fetch(`${API_BASE}/status`);
        const data = await response.json();
        
        // Inject Live GPS position into stadium data
        if (data.stadium.user) {
            data.stadium.user.pos = [userLivePos.x, userLivePos.y];
        }

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
            node.innerHTML = `
                <div id="user-arrow" style="position:absolute; top:50%; left:50%; width:0; height:0; border-left: 6px solid transparent; border-right: 6px solid transparent; border-bottom: 12px solid var(--primary); transform-origin: 50% 100%; transform: translate(-50%, -100%) rotate(${userHeading}deg); filter: drop-shadow(0 0 5px var(--primary));"></div>
                <div style="width:100%; height:100%; background:white; border-radius:50%; border:2px solid var(--primary); position:relative; z-index:2;"></div>
            `;
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
        node.onclick = () => {
            appendMessage('user', `How do I get to ${loc.name}?`);
            drawNavigationPath(userLivePos, { x: loc.pos[0], y: loc.pos[1] });
            sendMessage(`How do I get to ${loc.name}?`);
        };
        
        stadiumMap.appendChild(node);
    });
}

function drawNavigationPath(start, end) {
    const path = document.getElementById('active-path');
    if (!path) return;
    
    // Smooth Bezier curve for architectural feel
    const midX = (start.x + end.x) / 2;
    const midY = (start.y + end.y) / 2;
    const d = `M ${start.x}% ${start.y}% Q ${midX + 5}% ${midY - 5}% ${end.x}% ${end.y}%`;
    
    path.setAttribute('d', d);
    path.style.opacity = '0.8';
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
            body: JSON.stringify({ 
                query: text,
                pos: [userLivePos.x, userLivePos.y]
            })
        });
        const data = await response.json();
        
        // Replace typing with actual response
        const typingMsg = document.getElementById(typingId);
        if (typingMsg) {
            typingMsg.innerHTML = marked.parse(data.response);
        }
    } catch (err) {
        document.getElementById(typingId).textContent = "Sorry, I can't connect to the AI right now. Please try again later.";
    }
}

function appendMessage(text, side, id = null) {
    const msg = document.createElement('div');
    msg.className = `message ${side}`;
    if (id) msg.id = id;
    
    if (side === 'ai') {
        msg.innerHTML = marked.parse(text);
    } else {
        msg.textContent = text;
    }
    
    chatMessages.appendChild(msg);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

sendBtn.addEventListener('click', sendMessage);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});
