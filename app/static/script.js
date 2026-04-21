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
        
        // Prepare Data
        const formData = new FormData(form);
        const data = buildPayload(formData);
        
        // UI Loading state
        submitBtn.disabled = true;
        btnText.textContent = 'Generating...';
        loader.classList.remove('hidden');
        document.getElementById('result-container').classList.add('hidden');
        
        try {
            const response = await fetch('/api/v1/generate-resume', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'Failed to generate resume');
            }
            
            const result = await response.json();
            
            // Show result
            document.getElementById('resume-output').textContent = result.resume;
            document.getElementById('result-container').classList.remove('hidden');
            
            // Scroll to result
            document.getElementById('result-container').scrollIntoView({ behavior: 'smooth' });
            
        } catch (error) {
            alert(`Error: ${error.message}`);
        } finally {
            submitBtn.disabled = false;
            btnText.textContent = 'Generate ATS Resume';
            loader.classList.add('hidden');
        }
    });

    document.getElementById('copy-btn').addEventListener('click', () => {
        const text = document.getElementById('resume-output').textContent;
        navigator.clipboard.writeText(text).then(() => {
            const btn = document.getElementById('copy-btn');
            btn.textContent = 'Copied!';
            setTimeout(() => btn.textContent = 'Copy Text', 2000);
        });
    });
});

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
        const baseArray = formData.getAll(fields[0]);
        for (let i = 0; i < baseArray.length; i++) {
            const item = {};
            let hasValue = false;
            fields.forEach(field => {
                const val = formData.getAll(field)[i];
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
