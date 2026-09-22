/**
 * Frontend JavaScript Application Logic
 * Handles Chat interactions, quick suggestions, and live meeting sidebar sync.
 */

document.addEventListener("DOMContentLoaded", () => {
    const chatMessages = document.getElementById("chat-messages");
    const chatForm = document.getElementById("chat-form");
    const userInput = document.getElementById("user-input");
    const meetingsList = document.getElementById("meetings-list");
    const refreshBtn = document.getElementById("refresh-meetings-btn");
    const suggestionPills = document.querySelectorAll(".suggestion-pill");

    // Fetch initial scheduled meetings
    fetchMeetings();

    // Event Listener for Chat Form Submission
    chatForm.addEventListener("submit", async (e) => {
        e.preventDefault();
        const message = userInput.value.trim();
        if (!message) return;

        // Append User Message
        appendMessage("user", message);
        userInput.value = "";

        // Append Loading Indicator
        const loadingId = appendLoadingMessage();

        try {
            const response = await fetch("/api/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();
            removeMessage(loadingId);

            if (response.ok) {
                appendMessage("assistant", data.reply);
                // Refresh meeting list in sidebar after response
                fetchMeetings();
            } else {
                appendMessage("assistant", `⚠️ Error: ${data.detail || "Failed to process request"}`);
            }
        } catch (error) {
            removeMessage(loadingId);
            appendMessage("assistant", `⚠️ Connection error: ${error.message}`);
        }
    });

    // Handle Quick Suggestion Pills
    suggestionPills.forEach(pill => {
        pill.addEventListener("click", () => {
            const promptText = pill.getAttribute("data-prompt");
            userInput.value = promptText;
            chatForm.dispatchEvent(new Event("submit"));
        });
    });

    // Refresh Meetings Button
    refreshBtn.addEventListener("click", () => {
        fetchMeetings();
    });

    // Append Chat Message to UI
    function appendMessage(sender, text) {
        const msgDiv = document.createElement("div");
        msgDiv.classList.add("message", `${sender}-message`);

        const avatar = document.createElement("div");
        avatar.classList.add("avatar", sender === "user" ? "user-avatar" : "bot-avatar");
        avatar.innerHTML = sender === "user" 
            ? `<i class="fa-solid fa-user"></i>` 
            : `<i class="fa-solid fa-robot"></i>`;

        const content = document.createElement("div");
        content.classList.add("message-content");
        content.innerHTML = formatMarkdown(text);

        msgDiv.appendChild(avatar);
        msgDiv.appendChild(content);

        chatMessages.appendChild(msgDiv);
        scrollToBottom();
    }

    // Append Loading Indicator
    function appendLoadingMessage() {
        const id = "loading-" + Date.now();
        const msgDiv = document.createElement("div");
        msgDiv.classList.add("message", "assistant-message");
        msgDiv.id = id;

        msgDiv.innerHTML = `
            <div class="avatar bot-avatar"><i class="fa-solid fa-robot"></i></div>
            <div class="message-content">
                <i class="fa-solid fa-circle-notch fa-spin"></i> Agent thinking & checking calendar...
            </div>
        `;

        chatMessages.appendChild(msgDiv);
        scrollToBottom();
        return id;
    }

    // Remove Message Element by ID
    function removeMessage(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }

    // Auto-scroll Chat Window
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Fetch and render meetings in sidebar
    async function fetchMeetings() {
        try {
            const res = await fetch("/api/meetings");
            const data = await res.json();
            renderMeetingsSidebar(data.meetings || []);
        } catch (err) {
            console.error("Failed to fetch meetings:", err);
        }
    }

    // Render Meetings Sidebar Cards
    function renderMeetingsSidebar(meetings) {
        if (!meetings || meetings.length === 0) {
            meetingsList.innerHTML = `
                <div class="empty-state">
                    <i class="fa-regular fa-calendar-xmark"></i>
                    <p>No meetings booked yet</p>
                </div>
            `;
            return;
        }

        meetingsList.innerHTML = meetings.map(m => `
            <div class="meeting-card">
                <div class="meeting-card-header">
                    <span class="meeting-card-title">${escapeHtml(m.title)}</span>
                    <span class="meeting-card-id">${escapeHtml(m.meeting_id)}</span>
                </div>
                <div class="meeting-card-details">
                    <div class="meeting-detail-item">
                        <i class="fa-regular fa-calendar"></i>
                        <span>${escapeHtml(m.date)} at ${escapeHtml(m.time)}</span>
                    </div>
                    <div class="meeting-detail-item">
                        <i class="fa-regular fa-clock"></i>
                        <span>${m.duration_minutes} mins</span>
                    </div>
                    ${m.attendees && m.attendees.length > 0 ? `
                    <div class="meeting-detail-item">
                        <i class="fa-regular fa-user"></i>
                        <span>${m.attendees.join(", ")}</span>
                    </div>
                    ` : ''}
                </div>
            </div>
        `).join("");
    }

    // Simple Markdown Formatter
    function formatMarkdown(str) {
        if (!str) return "";
        return str
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`([^`]+)`/g, '<code>$1</code>')
            .replace(/\n\n/g, '<br><br>')
            .replace(/\n- /g, '<br>• ');
    }

    // Escape HTML Helper
    function escapeHtml(str) {
        return str ? str.replace(/[&<>"']/g, match => ({
            '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'
        }[match])) : '';
    }
});
