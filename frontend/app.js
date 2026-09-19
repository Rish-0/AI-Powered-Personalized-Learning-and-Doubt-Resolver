/* ============================================
   AI Tutor — Application Logic
   ============================================ */

const API_BASE = 'http://localhost:8000/api';

// --- State ---
const state = {
    username: localStorage.getItem('ai_tutor_username') || 'student',
    messages: [],
    isLoading: false,
    uploadedFiles: JSON.parse(localStorage.getItem('ai_tutor_files') || '[]'),
    profile: JSON.parse(localStorage.getItem('ai_tutor_profile') || '{}'),
};

// --- DOM Elements ---
const $ = (sel) => document.querySelector(sel);
const $$ = (sel) => document.querySelectorAll(sel);

const elements = {
    chatContainer: $('#chatContainer'),
    messages: $('#messages'),
    welcomeScreen: $('#welcomeScreen'),
    messageInput: $('#messageInput'),
    sendBtn: $('#sendBtn'),
    sidebar: $('#sidebar'),
    sidebarOverlay: $('#sidebarOverlay'),
    mobileMenuBtn: $('#mobileMenuBtn'),
    newChatBtn: $('#newChatBtn'),
    historyList: $('#historyList'),
    uploadedFilesList: $('#uploadedFilesList'),
    uploadBtn: $('#uploadBtn'),
    uploadModal: $('#uploadModal'),
    uploadModalClose: $('#uploadModalClose'),
    uploadZone: $('#uploadZone'),
    fileInput: $('#fileInput'),
    uploadProgress: $('#uploadProgress'),
    progressFill: $('#progressFill'),
    uploadStatus: $('#uploadStatus'),
    profileBtn: $('#profileBtn'),
    topProfileBtn: $('#topProfileBtn'),
    profileModal: $('#profileModal'),
    profileModalClose: $('#profileModalClose'),
    profileForm: $('#profileForm'),
    usernameInput: $('#usernameInput'),
    weakTopicsInput: $('#weakTopicsInput'),
    strongTopicsInput: $('#strongTopicsInput'),
    connectionStatus: $('#connectionStatus'),
};

// --- Initialize ---
document.addEventListener('DOMContentLoaded', () => {
    initApp();
});

function initApp() {
    setupEventListeners();
    loadProfile();
    loadHistory();
    renderUploadedFiles();
    checkBackendHealth();
}

// --- Event Listeners ---
function setupEventListeners() {
    // Send message
    elements.sendBtn.addEventListener('click', sendMessage);
    elements.messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Auto-resize textarea
    elements.messageInput.addEventListener('input', () => {
        const el = elements.messageInput;
        el.style.height = 'auto';
        el.style.height = Math.min(el.scrollHeight, 150) + 'px';
        elements.sendBtn.disabled = !el.value.trim();
    });

    // Sidebar toggle (mobile)
    elements.mobileMenuBtn.addEventListener('click', toggleSidebar);
    elements.sidebarOverlay.addEventListener('click', closeSidebar);

    // New chat
    elements.newChatBtn.addEventListener('click', newChat);

    // Upload modal
    elements.uploadBtn.addEventListener('click', () => openModal('uploadModal'));
    elements.uploadModalClose.addEventListener('click', () => closeModal('uploadModal'));

    // Upload zone
    elements.uploadZone.addEventListener('click', () => elements.fileInput.click());
    elements.fileInput.addEventListener('change', handleFileSelect);

    // Drag and drop
    elements.uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        elements.uploadZone.classList.add('drag-over');
    });
    elements.uploadZone.addEventListener('dragleave', () => {
        elements.uploadZone.classList.remove('drag-over');
    });
    elements.uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        elements.uploadZone.classList.remove('drag-over');
        if (e.dataTransfer.files.length) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    // Profile modal
    elements.profileBtn.addEventListener('click', () => openModal('profileModal'));
    elements.topProfileBtn.addEventListener('click', () => openModal('profileModal'));
    elements.profileModalClose.addEventListener('click', () => closeModal('profileModal'));

    // Profile form
    elements.profileForm.addEventListener('submit', handleProfileSave);

    // Difficulty buttons
    $$('.difficulty-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            $$('.difficulty-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });

    // Style buttons
    $$('.style-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            $$('.style-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });

    // Welcome cards
    $$('.welcome-card').forEach(card => {
        card.addEventListener('click', () => {
            const prompt = card.dataset.prompt;
            elements.messageInput.value = prompt;
            elements.sendBtn.disabled = false;
            sendMessage();
        });
    });

    // Close modals on overlay click
    $$('.modal-overlay').forEach(overlay => {
        overlay.addEventListener('click', (e) => {
            if (e.target === overlay) {
                overlay.classList.remove('active');
            }
        });
    });
}

// --- Chat ---
async function sendMessage() {
    const question = elements.messageInput.value.trim();
    if (!question || state.isLoading) return;

    // Hide welcome screen
    elements.welcomeScreen.classList.add('hidden');

    // Add user message
    addMessage('user', question);
    elements.messageInput.value = '';
    elements.messageInput.style.height = 'auto';
    elements.sendBtn.disabled = true;

    // Show typing indicator
    const typingEl = showTypingIndicator();
    state.isLoading = true;
    updateStatus('Thinking...');

    try {
        const response = await fetch(`${API_BASE}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                username: state.username,
                question: question,
            }),
        });

        if (!response.ok) throw new Error(`Server error: ${response.status}`);

        const data = await response.json();

        // Remove typing indicator
        typingEl.remove();

        // Add AI message
        addMessage('ai', data.answer, {
            route: data.route,
            sources: data.sources,
        });

        // Refresh history
        loadHistory();

    } catch (error) {
        console.error('Chat error:', error);
        typingEl.remove();
        addMessage('ai', '⚠️ Sorry, I couldn\'t process your question. Please make sure the backend server is running at `http://localhost:8000`.\n\n**Error:** ' + error.message, {
            route: 'ERROR',
        });
    } finally {
        state.isLoading = false;
        updateStatus('Ready');
    }
}

function addMessage(type, content, meta = {}) {
    const msg = { type, content, meta, timestamp: new Date() };
    state.messages.push(msg);

    const messageEl = document.createElement('div');
    messageEl.className = `message ${type}`;

    const avatarEmoji = type === 'user' ? '👤' : '🎓';

    let parsedContent = content;
    if (type === 'ai') {
        try {
            parsedContent = marked.parse(content);
        } catch (e) {
            parsedContent = content.replace(/\n/g, '<br>');
        }
    } else {
        parsedContent = escapeHtml(content);
    }

    let routeBadge = '';
    if (meta.route && meta.route !== 'ERROR') {
        const routeClass = meta.route.toLowerCase();
        const routeLabels = {
            'pdf_rag': '📄 PDF Source',
            'web_search': '🌐 Web Search',
            'general_chat': '💬 General Chat',
        };
        routeBadge = `<div class="message-route ${routeClass}">${routeLabels[routeClass] || meta.route}</div>`;
    }

    let sourcesHtml = '';
    if (meta.sources && meta.sources.length > 0 && meta.route === 'PDF_RAG') {
        const sourceItems = meta.sources.map(s => {
            if (s.page !== undefined) {
                return `<div class="source-item">📄 <span>${s.source || 'Document'}</span> — Page ${s.page}</div>`;
            }
            return '';
        }).filter(Boolean).join('');

        if (sourceItems) {
            sourcesHtml = `
                <div class="message-sources">
                    <div class="message-sources-title">Sources</div>
                    ${sourceItems}
                </div>
            `;
        }
    }

    if (meta.sources && meta.sources.length > 0 && meta.route === 'WEB_SEARCH') {
        const sourceItems = meta.sources.slice(0, 3).map(s => {
            if (s.title) {
                return `<div class="source-item">🌐 <span>${s.title}</span></div>`;
            }
            return '';
        }).filter(Boolean).join('');

        if (sourceItems) {
            sourcesHtml = `
                <div class="message-sources">
                    <div class="message-sources-title">Web Sources</div>
                    ${sourceItems}
                </div>
            `;
        }
    }

    messageEl.innerHTML = `
        <div class="message-avatar">${avatarEmoji}</div>
        <div class="message-content">
            <div class="message-bubble">${parsedContent}</div>
            ${routeBadge}
            ${sourcesHtml}
        </div>
    `;

    elements.messages.appendChild(messageEl);
    scrollToBottom();
}

function showTypingIndicator() {
    const el = document.createElement('div');
    el.className = 'message ai';
    el.innerHTML = `
        <div class="message-avatar">🎓</div>
        <div class="message-content">
            <div class="message-bubble">
                <div class="typing-indicator">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        </div>
    `;
    elements.messages.appendChild(el);
    scrollToBottom();
    return el;
}

function scrollToBottom() {
    elements.chatContainer.scrollTop = elements.chatContainer.scrollHeight;
}

function newChat() {
    state.messages = [];
    elements.messages.innerHTML = '';
    elements.welcomeScreen.classList.remove('hidden');
    closeSidebar();
}

// --- History ---
async function loadHistory() {
    try {
        const response = await fetch(`${API_BASE}/history?limit=20`);
        if (!response.ok) return;

        const history = await response.json();
        renderHistory(history);
    } catch (error) {
        console.log('Could not load history:', error.message);
    }
}

function renderHistory(history) {
    if (!history.length) {
        elements.historyList.innerHTML = '<p class="empty-state-text">No conversations yet</p>';
        return;
    }

    elements.historyList.innerHTML = history.map(item => {
        const routeClass = (item.route || '').toLowerCase();
        const icons = {
            'pdf_rag': '📄',
            'web_search': '🌐',
            'general_chat': '💬',
        };
        const icon = icons[routeClass] || '💬';

        return `
            <div class="history-item" data-question="${escapeAttr(item.question)}" data-answer="${escapeAttr(item.answer)}" data-route="${escapeAttr(item.route || '')}">
                <div class="history-item-icon ${routeClass}">${icon}</div>
                <div class="history-item-text">${escapeHtml(item.question)}</div>
            </div>
        `;
    }).join('');

    // Click to load conversation
    elements.historyList.querySelectorAll('.history-item').forEach(item => {
        item.addEventListener('click', () => {
            elements.welcomeScreen.classList.add('hidden');

            // Show the Q&A from history
            const question = item.dataset.question;
            const answer = item.dataset.answer;
            const route = item.dataset.route;

            addMessage('user', question);
            addMessage('ai', answer, { route });
            closeSidebar();
        });
    });
}

// --- File Upload ---
function handleFileSelect(e) {
    if (e.target.files.length) {
        handleFile(e.target.files[0]);
    }
}

async function handleFile(file) {
    if (!file.name.endsWith('.pdf')) {
        showToast('Only PDF files are allowed', 'error');
        return;
    }

    if (file.size > 20 * 1024 * 1024) {
        showToast('File size must be under 20 MB', 'error');
        return;
    }

    // Show progress
    elements.uploadProgress.style.display = 'block';
    elements.uploadStatus.textContent = 'Uploading & indexing...';
    elements.uploadStatus.className = 'upload-status';
    elements.progressFill.style.width = '30%';

    const formData = new FormData();
    formData.append('file', file);

    try {
        // Simulate progress
        elements.progressFill.style.width = '60%';

        const response = await fetch(`${API_BASE}/upload`, {
            method: 'POST',
            body: formData,
        });

        elements.progressFill.style.width = '90%';

        if (!response.ok) throw new Error('Upload failed');

        const data = await response.json();

        elements.progressFill.style.width = '100%';
        elements.uploadStatus.textContent = `✓ Indexed ${data.pages} pages, ${data.chunks} chunks`;
        elements.uploadStatus.className = 'upload-status success';

        // Track uploaded file
        const fileInfo = { name: file.name, pages: data.pages, chunks: data.chunks };
        state.uploadedFiles.push(fileInfo);
        localStorage.setItem('ai_tutor_files', JSON.stringify(state.uploadedFiles));
        renderUploadedFiles();

        showToast(`${file.name} uploaded successfully!`, 'success');

        // Auto-close modal after delay
        setTimeout(() => {
            closeModal('uploadModal');
            // Reset upload zone
            elements.uploadProgress.style.display = 'none';
            elements.progressFill.style.width = '0%';
        }, 2000);

    } catch (error) {
        elements.uploadStatus.textContent = '✗ Upload failed. Is the backend running?';
        elements.uploadStatus.className = 'upload-status error';
        elements.progressFill.style.width = '0%';
        showToast('Upload failed: ' + error.message, 'error');
    }
}

function renderUploadedFiles() {
    if (!state.uploadedFiles.length) {
        elements.uploadedFilesList.innerHTML = '<p class="empty-state-text">No files uploaded yet</p>';
        return;
    }

    elements.uploadedFilesList.innerHTML = state.uploadedFiles.map(file => `
        <div class="file-item">
            <span class="file-item-icon">📕</span>
            <span class="file-item-name">${escapeHtml(file.name)}</span>
        </div>
    `).join('');
}

// --- Profile ---
function loadProfile() {
    const saved = state.profile;
    if (saved.username) {
        state.username = saved.username;
        elements.usernameInput.value = saved.username;
    }
    if (saved.difficulty) {
        $$('.difficulty-btn').forEach(b => {
            b.classList.toggle('active', b.dataset.value === saved.difficulty);
        });
    }
    if (saved.learning_style) {
        $$('.style-btn').forEach(b => {
            b.classList.toggle('active', b.dataset.value === saved.learning_style);
        });
    }
    if (saved.weak_topics) {
        elements.weakTopicsInput.value = saved.weak_topics;
    }
    if (saved.strong_topics) {
        elements.strongTopicsInput.value = saved.strong_topics;
    }
}

async function handleProfileSave(e) {
    e.preventDefault();

    const username = elements.usernameInput.value.trim() || 'student';
    const difficulty = $('.difficulty-btn.active')?.dataset.value || 'medium';
    const learningStyle = $('.style-btn.active')?.dataset.value || 'textual';
    const weakTopics = elements.weakTopicsInput.value.trim();
    const strongTopics = elements.strongTopicsInput.value.trim();

    state.username = username;

    const profileData = {
        username,
        difficulty,
        learning_style: learningStyle,
        weak_topics: weakTopics,
        strong_topics: strongTopics,
    };

    // Save locally
    state.profile = profileData;
    localStorage.setItem('ai_tutor_username', username);
    localStorage.setItem('ai_tutor_profile', JSON.stringify(profileData));

    // Save to backend
    try {
        await fetch(`${API_BASE}/profile`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(profileData),
        });
        showToast('Profile saved successfully!', 'success');
    } catch (error) {
        showToast('Profile saved locally (backend unavailable)', 'error');
    }

    closeModal('profileModal');
}

// --- Backend Health Check ---
async function checkBackendHealth() {
    try {
        const response = await fetch('http://localhost:8000/health');
        if (response.ok) {
            updateStatus('Ready');
        } else {
            updateStatus('Server error');
        }
    } catch {
        updateStatus('Backend offline');
        elements.connectionStatus.querySelector('.status-dot').style.background = 'var(--danger)';
    }
}

function updateStatus(text) {
    const statusEl = elements.connectionStatus;
    const dot = statusEl.querySelector('.status-dot');

    statusEl.childNodes[statusEl.childNodes.length - 1].textContent = ' ' + text;

    if (text === 'Ready') {
        dot.style.background = 'var(--success)';
    } else if (text === 'Thinking...') {
        dot.style.background = 'var(--warning)';
    } else {
        dot.style.background = 'var(--danger)';
    }
}

// --- Sidebar ---
function toggleSidebar() {
    elements.sidebar.classList.toggle('open');
    elements.sidebarOverlay.classList.toggle('active');
}

function closeSidebar() {
    elements.sidebar.classList.remove('open');
    elements.sidebarOverlay.classList.remove('active');
}

// --- Modals ---
function openModal(id) {
    $(`#${id}`).classList.add('active');
}

function closeModal(id) {
    $(`#${id}`).classList.remove('active');
}

// --- Toast Notifications ---
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}

// --- Utility ---
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function escapeAttr(text) {
    return text
        .replace(/&/g, '&amp;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
}
