// Populate projects dynamically
document.addEventListener('DOMContentLoaded', () => {
    const projectsContainer = document.querySelector('.projects');
    if (!projectsContainer) return;

    const projects = [
        {
            title: 'NNPC Headquarters',
            images: ['BROCHURE_Page_069_Image_0002.png', 'BROCHURE_Page_069_Image_0001.png', 'BROCHURE_Page_069_Image_0003.png', 'BROCHURE_Page_069_Image_0004.png']
        },
        {
            title: 'River Plaza & Mall',
            images: ['BROCHURE_Page_074_Image_0001.png', 'BROCHURE_Page_074_Image_0002.png', '05ea8acbcb7c39-river-plaza-and-mall-11storey-building-plaza-complex-mall-for-sale-central-business-district-abuja.jpg']
        },
        {
            title: 'Government Complex',
            images: ['BROCHURE_Page_084_Image_0001 - Copy.png', 'BROCHURE_Page_084_Image_0002 - Copy.png', 'BROCHURE_Page_084_Image_0003 - Copy.png']
        },
        {
            title: 'Residential Development',
            images: ['BROCHURE_Page_112_Image_0001 - Copy.png', 'BROCHURE_Page_112_Image_0002 - Copy.png', 'BROCHURE_Page_112_Image_0003 - Copy.png']
        }
    ];

    projects.forEach((project) => {
        const projectEl = document.createElement('div');
        projectEl.className = 'project';
        projectEl.innerHTML = `
            <h3 class="project-title">${project.title}</h3>
            <div class="project-gallery">
                <div class="project-gallery-track">
                    ${project.images.map(img => `<img src="media/Build/${img}" alt="${project.title}" class="project-image" loading="lazy">`).join('')}
                </div>
            </div>`;
        projectsContainer.appendChild(projectEl);
    });
});
