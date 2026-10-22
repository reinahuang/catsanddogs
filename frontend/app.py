# app.py (前端 UI)
import os
from flask import Flask, render_template_string

app = Flask(__name__)

# 通用 CSS 样式
COMMON_STYLE = """
<style>
    body { font-family: Arial, sans-serif; max-width: 600px; margin: 40px auto; padding: 20px; }
    .card { border: 1px solid #ddd; padding: 25px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .form-group { margin-bottom: 15px; }
    label { display: block; margin-bottom: 5px; font-weight: bold; }
    input[type="text"] { width: 95%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
    button { padding: 10px 20px; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; }
    .btn-cat { background-color: #28a745; }
    .btn-dog { background-color: #17a2b8; }
    ul { list-style-type: none; padding: 0; }
    li { background: #f8f9fa; margin: 5px 0; padding: 10px; border-radius: 4px; border-left: 4px solid #333; }
</style>
"""

# 1. /cat 视图模板
CAT_TEMPLATE = COMMON_STYLE + """
<div class="card">
    <h1>🐱 Welcome to Cat's world</h1>
    <hr>
    <div class="form-group">
        <label>Your Name:</label>
        <input type="text" id="ownerName" placeholder="Enter your name...">
    </div>
    <div class="form-group">
        <label>What's the name of your cat?</label>
        <input type="text" id="petName" placeholder="Enter cat's name...">
    </div>
    <button class="btn-cat" onclick="submitCat()">Register Cat</button>

    <h3>Registered Cats:</h3>
    <ul id="catsList">Loading...</ul>
</div>

<script>
    async function loadCats() {
        try {
            const res = await fetch('/api/cats');
            const data = await res.json();
            const listEl = document.getElementById('catsList');
            listEl.innerHTML = '';
            if (data.length === 0) { listEl.innerHTML = '<li>No cats registered yet.</li>'; return; }
            data.forEach(item => {
                const li = document.createElement('li');
                li.textContent = `Owner: ${item.owner_name} | Cat Name: ${item.cat_name}`;
                listEl.appendChild(li);
            });
        } catch(e) { console.error(e); }
    }

    async function submitCat() {
        const ownerName = document.getElementById('ownerName').value.trim();
        const petName = document.getElementById('petName').value.trim();
        if (!ownerName || !petName) { alert('Please fill in both fields!'); return; }

        const res = await fetch('/api/cats', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ owner_name: ownerName, cat_name: petName })
        });
        if (res.ok) {
            document.getElementById('ownerName').value = '';
            document.getElementById('petName').value = '';
            loadCats();
        }
    }
    loadCats();
</script>
"""

# 2. /dog 视图模板
DOG_TEMPLATE = COMMON_STYLE + """
<div class="card">
    <h1>🐶 Welcome to Dog's world</h1>
    <hr>
    <div class="form-group">
        <label>Your Name:</label>
        <input type="text" id="ownerName" placeholder="Enter your name...">
    </div>
    <div class="form-group">
        <label>What's the name of your dog?</label>
        <input type="text" id="petName" placeholder="Enter dog's name...">
    </div>
    <button class="btn-dog" onclick="submitDog()">Register Dog</button>

    <h3>Registered Dogs:</h3>
    <ul id="dogsList">Loading...</ul>
</div>

<script>
    async function loadDogs() {
        try {
            const res = await fetch('/api/dogs');
            const data = await res.json();
            const listEl = document.getElementById('dogsList');
            listEl.innerHTML = '';
            if (data.length === 0) { listEl.innerHTML = '<li>No dogs registered yet.</li>'; return; }
            data.forEach(item => {
                const li = document.createElement('li');
                li.textContent = `Owner: ${item.owner_name} | Dog Name: ${item.dog_name}`;
                listEl.appendChild(li);
            });
        } catch(e) { console.error(e); }
    }

    async function submitDog() {
        const ownerName = document.getElementById('ownerName').value.trim();
        const petName = document.getElementById('petName').value.trim();
        if (!ownerName || !petName) { alert('Please fill in both fields!'); return; }

        const res = await fetch('/api/dogs', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ owner_name: ownerName, dog_name: petName })
        });
        if (res.ok) {
            document.getElementById('ownerName').value = '';
            document.getElementById('petName').value = '';
            loadDogs();
        }
    }
    loadDogs();
</script>
"""

@app.route('/')
def index():
    return COMMON_STYLE + """
    <div class="card">
        <h1>🐾 Pet World App</h1>
        <p>Choose your world:</p>
        <ul>
            <li><a href="/cat">🐱 Visit Cat's World</a></li>
            <li><a href="/dog">🐶 Visit Dog's World</a></li>
        </ul>
    </div>
    """

@app.route('/cat')
def cat_page():
    return render_template_string(CAT_TEMPLATE)

@app.route('/dog')
def dog_page():
    return render_template_string(DOG_TEMPLATE)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)