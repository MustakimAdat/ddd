// TOGGLE SIDEBAR
const menuBar = document.querySelector('#content nav .bx.bx-menu');
const sidebar = document.getElementById('sidebar');
    menuBar.addEventListener('click', function () {
        sidebar.classList.toggle('hide');
    })

    const allSideMenu = document.querySelectorAll('#sidebar .side-menu.top li a');
    allSideMenu.forEach(item=> {
        const li = item.parentElement;
            item.addEventListener('click', function () {
                allSideMenu.forEach(i=> {
                    i.parentElement.classList.remove('active');
                })
                li.classList.add('active');
            })
        });

    
        document.getElementById('profileImage').addEventListener('click', function(event) {
            event.preventDefault();
            const dropdown = document.querySelector('.profile-dropdown');
            dropdown.classList.toggle('show');
        });
        
        window.onclick = function(event) {
            if (!event.target.matches('#profileImage')) {
                const dropdowns = document.querySelectorAll('.dropdown-content');
                dropdowns.forEach(function(dropdown) {
                    if (dropdown.parentElement.classList.contains('show')) {
                        dropdown.parentElement.classList.remove('show');
                    }
                });
            }
        }
        document.getElementById('roleToggle').addEventListener('change', function() {
            const roleText = document.getElementById('roleText');
            if (this.checked) {
                roleText.textContent = 'Admin';
            } else {
                roleText.textContent = 'User';
            }
        });
        