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
            summaryText.textContent = result.summary;

            // Update data table
            dataTableContainer.innerHTML = createTableFromData(result.data_result);

        } catch (error) {
            summaryText.textContent = `An error occurred: ${error.message}`;
            dataTableContainer.innerHTML = '';
        } finally {
            // Hide loading indicator
            loadingIndicator.classList.add('hidden');
            resultsContainer.classList.remove('hidden');
        }
    };

    function createTableFromData(data) {
        // This is a simplistic parser. A real app would need a more robust one.
        try {
            // LangChain often returns a string representation of a list of tuples.
            const rows = JSON.parse(data.replace(/'/g, '"'));
            if (!Array.isArray(rows) || rows.length === 0) return '<p>No data returned.</p>';

            // This is a huge assumption about the data structure.
            // A better approach would be to get headers from the DB schema.
            // For the MVP, we assume the structure is consistent.
            let table = '<table>';
            // Note: We don't have headers here. A real app would need them.
            // We'll just display the rows.
            rows.forEach(row => {
                table += '<tr>';
                row.forEach(cell => {
                    table += `<td>${cell}</td>`;
                });
                table += '</tr>';
            });
            table += '</table>';
            return table;
        } catch (e) {
            return `<p>Could not parse data:</p><pre>${data}</pre>`;
        }
    }

    sendBtn.addEventListener('click', handleSend);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            handleSend();
        }
    });
});

