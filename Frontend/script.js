// frontend/script.js
document.addEventListener('DOMContentLoaded', () => {
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const chatHistory = document.getElementById('chat-history');
    const summaryText = document.getElementById('summary-text');
    const dataTableContainer = document.getElementById('data-table-container');
    const loadingIndicator = document.getElementById('loading-indicator');
    const resultsContainer = document.getElementById('results-container');

    const handleSend = async () => {
        const question = userInput.value.trim();
        if (!question) return;

        // Add user message to chat
        const userMessage = document.createElement('div');
        userMessage.className = 'message user';
        userMessage.innerHTML = `<p>${question}</p>`;
        chatHistory.appendChild(userMessage);
        userInput.value = '';
        chatHistory.scrollTop = chatHistory.scrollHeight;

        // Show loading indicator
        loadingIndicator.classList.remove('hidden');
        resultsContainer.classList.add('hidden');

        try {
            const response = await fetch('/query', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: question })
            });
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const result = await response.json();

            // Update summary
            summaryText.textContent = result.summary || 'No summary available.';

            // Update data table from structured JSON array
            dataTableContainer.innerHTML = createTableFromJsonRows(result.data_result);

        } catch (error) {
            summaryText.textContent = `An error occurred: ${error.message}`;
            dataTableContainer.innerHTML = '';
        } finally {
            // Hide loading indicator
            loadingIndicator.classList.add('hidden');
            resultsContainer.classList.remove('hidden');
        }
    };

    // Expect data_result to be an array of arrays (rows)
    function createTableFromJsonRows(rows) {
        try {
            if (!Array.isArray(rows) || rows.length === 0) {
                return '<p>No data returned.</p>';
            }

            let table = '<table>';
            rows.forEach(row => {
                table += '<tr>';
                if (Array.isArray(row)) {
                    row.forEach(cell => {
                        table += `<td>${escapeHtml(String(cell))}</td>`;
                    });
                } else if (row && typeof row === 'object') {
                    Object.values(row).forEach(cell => {
                        table += `<td>${escapeHtml(String(cell))}</td>`;
                    });
                } else {
                    table += `<td>${escapeHtml(String(row))}</td>`;
                }
                table += '</tr>';
            });
            table += '</table>';
            return table;
        } catch (e) {
            return `<p>Could not render rows.</p><pre>${e.message}</pre>`;
        }
    }

    function escapeHtml(unsafe) {
        return unsafe
            .replaceAll(/&/g, "&amp;")
            .replaceAll(/</g, "&lt;")
            .replaceAll(/>/g, "&gt;")
            .replaceAll(/"/g, "&quot;")
            .replaceAll(/'/g, "&#039;");
    }

    sendBtn.addEventListener('click', handleSend);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSend();
        }
    });
});
