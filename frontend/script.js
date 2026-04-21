document.addEventListener('DOMContentLoaded', () => {
    // Add initial dynamic fields
    addEducation();
    addProject();

    const form = document.getElementById('resume-form');
    
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const submitBtn = document.getElementById('submit-btn');
        const loader = submitBtn.querySelector('.loader');
        const btnText = submitBtn.querySelector('.btn-text');
        const placeholder = document.getElementById('resume-placeholder');
        const output = document.getElementById('resume-output');
        
        // Prepare Data
        const formData = new FormData(form);
        const data = buildPayload(formData);
        
        // UI Loading state
        submitBtn.disabled = true;
        btnText.textContent = 'Generating...';
        loader.classList.remove('hidden');
        
        // Keep current view while loading
        
        try {
            const response = await fetch('http://localhost:8000/api/v1/generate-resume', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                let errMsg = 'Failed to generate resume';
                if (errorData.detail) {
                    if (Array.isArray(errorData.detail)) {
                        errMsg = errorData.detail.map(e => `${e.loc ? e.loc.join('.') : 'Field'}: ${e.msg}`).join('\n');
                    } else {
                        errMsg = typeof errorData.detail === 'string' ? errorData.detail : JSON.stringify(errorData.detail);
                    }
                }
                throw new Error(errMsg);
            }
            
            const result = await response.json();
            
            // Show result
            placeholder.classList.add('hidden');
            
            // Render Markdown
            output.innerHTML = marked.parse(result.resume);
            output.classList.remove('hidden');
            
            // Show Actions
            document.getElementById('resume-actions').classList.remove('hidden');
            
            // Scroll to top of result on mobile
            if (window.innerWidth <= 1024) {
                document.getElementById('result-container').scrollIntoView({ behavior: 'smooth' });
            }
            
        } catch (error) {
            alert(`Error: ${error.message}`);
        } finally {
            submitBtn.disabled = false;
            btnText.textContent = 'Generate Stylish Resume';
            loader.classList.add('hidden');
        }
    });

    // Copy Content
    document.getElementById('copy-btn').addEventListener('click', () => {
        const textArea = document.getElementById('resume-output');
        const text = textArea.innerText || textArea.textContent;
        if (!text) return;
        
        navigator.clipboard.writeText(text).then(() => {
            const btn = document.getElementById('copy-btn');
            const originalText = btn.textContent;
            btn.textContent = 'Copied!';
            
            setTimeout(() => {
                btn.textContent = originalText;
            }, 2000);
        });
    });

    // Print Functionality
    document.getElementById('print-btn')?.addEventListener('click', () => {
        window.print();
    });
});

/**
 * Toggle collapsible form sections
 */
function toggleSection(button) {
    const section = button.closest('.form-section');
    const isActive = section.classList.contains('active');
    
    // Optional: Close other sections (Accordion style)
    // document.querySelectorAll('.form-section').forEach(s => s.classList.remove('active'));
    
    if (isActive) {
        section.classList.remove('active');
    } else {
        section.classList.add('active');
    }
}

function addProfile() {
    const template = document.getElementById('profile-template');
    const clone = template.content.cloneNode(true);
    document.getElementById('profiles-container').appendChild(clone);
}

function addEducation() {
    const template = document.getElementById('education-template');
    const clone = template.content.cloneNode(true);
    document.getElementById('education-container').appendChild(clone);
}

function addProject() {
    const template = document.getElementById('project-template');
    const clone = template.content.cloneNode(true);
    document.getElementById('projects-container').appendChild(clone);
}

function addCertification() {
    const template = document.getElementById('certification-template');
    const clone = template.content.cloneNode(true);
    document.getElementById('certifications-container').appendChild(clone);
}

function buildPayload(formData) {
    const getList = (prefix, fields) => {
        const items = [];
        const baseArray = formData.getAll(fields[0] + '[]');
        if (!baseArray) return items;
        
        for (let i = 0; i < baseArray.length; i++) {
            const item = {};
            let hasValue = false;
            fields.forEach(field => {
                const vals = formData.getAll(field + '[]');
                const val = vals[i];
                if (val && val.trim() !== '') {
                    item[field.replace(prefix, '')] = val.trim();
                    hasValue = true;
                }
            });
            if (hasValue) items.push(item);
        }
        return items;
    };

    const payload = {
        name: formData.get('name'),
        email: formData.get('email'),
        phone: formData.get('phone'),
        location: formData.get('location'),
        summary: formData.get('summary') || undefined,
        skills: {
            languages: formData.get('languages') || undefined,
            web_dev: formData.get('web_dev') || undefined,
            ml_ai: formData.get('ml_ai') || undefined,
            libraries: formData.get('libraries') || undefined,
            tools_dbs: formData.get('tools_dbs') || undefined,
        },
        profiles: getList('profile_', ['profile_platform', 'profile_link']),
        education: getList('edu_', ['edu_degree', 'edu_institution', 'edu_year', 'edu_score']),
        projects: getList('proj_', ['proj_role', 'proj_name', 'proj_tech_stack', 'proj_description', 'proj_impact']),
        certifications: formData.getAll('cert_detail[]').filter(c => c.trim() !== '')
    };

    return payload;
}

