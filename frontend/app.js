const API_URL = 'http://127.0.0.1:8000';
let currentDocId = null;

document.addEventListener('DOMContentLoaded', () => {
    loadDocuments();
})

async function uploadPDF() {
    const fileInput = document.getElementById('pdfFile');
    const file = fileInput.files[0];

    if (!file) {
        alert('Please select a PDF file.');
        return;
    }

    const uploadBtn = document.getElementById('uploadBtn');
    const statusDiv = document.getElementById('uploadStatus');
    console.log("Uploading PDF...")
    uploadBtn.disabled = true;
    statusDiv.innerHTML = 'Uploading and processing...'
    statusDiv.className = 'status-loading'
    statusDiv.style.display = 'block'

    const formData = new FormData();
    formData.append('file', file);

    url = `${API_URL}/documents/upload/`
    console.log(url)


    try {
        const response = await fetch(url, {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            // Update status
            statusDiv.innerHTML = `${result.message}`;
            statusDiv.className = 'status-success';
            
            // Show document info
            document.getElementById('docInfo').style.display = 'block';
            document.getElementById('docName').textContent = result.filename;
            document.getElementById('docChunks').textContent = result.chunks_count;
            
            // Clear messages
            document.getElementById('messages').innerHTML = '';
            
            // Add welcome message
            addMessage('assistant', `Document "${result.filename}" loaded! You can now ask questions about it.`);
        } else {
            statusDiv.innerHTML = `Error: ${result.detail}`;
            statusDiv.className = 'status-error';
        }
        } catch (error) {
        statusDiv.innerHTML = `❌ Network error: ${error.message}`;
        statusDiv.className = 'status-error';
    } finally {
        uploadBtn.disabled = false;
    }
    window.location = window.location;
}

async function sendQuery() {
    const input = document.getElementById('queryInput');
    const question = input.value.trim();
    console.log("Question:", question);
    if (!question) return;
    
    
    
    const sendBtn = document.getElementById('sendBtn');
    sendBtn.disabled = true;
    
    // Add user message
    addMessage('user', question);
    input.value = '';
    
    // Add loading indicator
    const loadingId = addMessage('assistant', 'Thinking...');

    console.log("BODY:", {
        question: question,
        document_id: null
    });
    
    try {
        const response = await fetch(`${API_URL}/chat/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question: question,
                document_id: null
            })
        });
        
        const result = await response.json();
        console.log("STATUS:", response.status);
        console.log("BODY:", result);
        
        // Remove loading message
        document.getElementById(loadingId).remove();
        
        if (response.ok) {
            // Add answer with sources
            addMessageWithSources(result.answer, result.sources);
        } else {
            addMessage('assistant', `Error: ${result.detail}`);
        }
        
    } catch (error) {
        document.getElementById(loadingId).remove();
        addMessage('assistant', `Network error: ${error.message}`);
    } finally {
        sendBtn.disabled = false;
    }
}

function addMessage(role, text) {
    const messagesDiv = document.getElementById('messages');
    const messageId = `msg-${Date.now()}`;
    
    const messageDiv = document.createElement('div');
    messageDiv.id = messageId;
    messageDiv.className = `message ${role}`;
    messageDiv.textContent = text;
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    
    return messageId;
}

function addMessageWithSources(answer, sources) {
    const messagesDiv = document.getElementById('messages');
    
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';
    
    // Answer text
    const answerText = document.createElement('div');
    answerText.textContent = answer;
    messageDiv.appendChild(answerText);
    
    // Sources
    if (sources && sources.length > 0) {
        const sourcesDiv = document.createElement('div');
        sourcesDiv.className = 'sources';
        
        const sourcesTitle = document.createElement('div');
        sourcesTitle.innerHTML = '<strong>📄 Sources:</strong>';
        sourcesDiv.appendChild(sourcesTitle);
        
        sources.forEach((source, idx) => {
            const sourceItem = document.createElement('div');
            sourceItem.className = 'source-item';
            sourceItem.innerHTML = `
                <strong>Page ${source.page}</strong> (relevance: ${(1 - source.score).toFixed(2)})<br>
                <small>${source.text.substring(0, 150)}...</small>
            `;
            sourcesDiv.appendChild(sourceItem);
        });
        
        messageDiv.appendChild(sourcesDiv);
    }
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendQuery();
    }
}

    
async function loadDocuments() {

    try {
        const response = await fetch(`${API_URL}/document/getall`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const documents = await response.json();
        renderDocuments(documents);
    }
    catch (error) {
        console.error('Error loading documents:', error);
    }
}

function renderDocuments(documents) {
    const tBody = document.getElementById("documentsBody");
    tBody.innerHTML = "";

    documents.forEach(doc => {
        const row = document.createElement("tr");

        row.innerHTML = 
        "<td><input type='checkbox' class='doc-checkbox' data-uuid='" + doc.uuid + "'></input></td>" +
        "<td>"+ doc.uuid +"</td>" +
        "<td>"+ doc.title +"</td>" +
        "<td>"+ doc.status +"</td>" +
        "<td>"+ doc.time +"</td>";

        tBody.appendChild(row);
    });
}

function deleteDocuments() {
    const checkboxes = document.querySelectorAll(".doc-checkbox:checked");
    const uuids = [];
    console.log(checkboxes);


    checkboxes.forEach(cb => {
        const uuid = cb.getAttribute("data-uuid");
        uuids.push(uuid);

    })
    console.log(uuids);

    try {
        const response = fetch(`${API_URL}/document/delete`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(uuids)}
        )}
    catch (error) {
        console.error('Error loading documents:', error);           
    }
    window.location = window.location;

}




  
    
