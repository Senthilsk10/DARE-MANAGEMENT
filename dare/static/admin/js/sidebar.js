
document.addEventListener('DOMContentLoaded', function() {
    // Mobile sidebar elements
    const sidebarToggle = document.getElementById('sidebarToggle');
    const sidebarBackdrop = document.getElementById('sidebarBackdrop');
    const mobileSidebar = document.getElementById('mobileSidebar');
    const closeSidebar = document.getElementById('closeSidebar');

    // Toggle sidebar function
    function toggleSidebar() {
        mobileSidebar.classList.toggle('-translate-x-full');
        sidebarBackdrop.classList.toggle('hidden');
        document.body.classList.toggle('overflow-hidden');
    }

    // Event listeners
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', toggleSidebar);
    }
    if (sidebarBackdrop) {
        sidebarBackdrop.addEventListener('click', toggleSidebar);
    }
    if (closeSidebar) {
        closeSidebar.addEventListener('click', toggleSidebar);
    }
});