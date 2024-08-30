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





// TOGGLE SIDEBAR
const menuBar = document.querySelector('#content nav .bx.bx-menu');
const sidebar = document.getElementById('sidebar');

menuBar.addEventListener('click', function () {
	sidebar.classList.toggle('hide');
})







const searchButton = document.querySelector('#content nav form .form-input button');
const searchButtonIcon = document.querySelector('#content nav form .form-input button .bx');
const searchForm = document.querySelector('#content nav form');

searchButton.addEventListener('click', function (e) {
	if(window.innerWidth < 576) {
		e.preventDefault();
		searchForm.classList.toggle('show');
		if(searchForm.classList.contains('show')) {
			searchButtonIcon.classList.replace('bx-search', 'bx-x');
		} else {
			searchButtonIcon.classList.replace('bx-x', 'bx-search');
		}
	}
})





if(window.innerWidth < 768) {
	sidebar.classList.add('hide');
} else if(window.innerWidth > 576) {
	searchButtonIcon.classList.replace('bx-x', 'bx-search');
	searchForm.classList.remove('show');
}


window.addEventListener('resize', function () {
	if(this.innerWidth > 576) {
		searchButtonIcon.classList.replace('bx-x', 'bx-search');
		searchForm.classList.remove('show');
	}
})

function openForm(){
    window.open("form.html")
}



//const switchMode = document.getElementById('switch-mode');

//switchMode.addEventListener('change', function () {
//	if(this.checked) {
//		document.body.classList.add('dark');
//	} else {
//		document.body.classList.remove('dark');
//	}
//})




function updateSecondDropdown() {
    var departmentDropdown = document.getElementById("department");
    var subCategoryDropdown = document.getElementById("subCategory");
    var department = departmentDropdown.value;
  
    // Clearing previous options
    subCategoryDropdown.innerHTML = '<option value="">Select Subcategory</option>';
  
    // Adding options based on department selection
    if (department === "IT") {
      subCategoryDropdown.innerHTML += `
        <option value="Hardware">Hardware</option>
        <option value="Software">Software</option>
        <option value="Network">Network</option>
        <option value="Printer">Printer</option>
        <option value="Projector">Projector</option>
        <option value="Other">Other</option>
      `;
    } else if (department === "Electrical") {
      subCategoryDropdown.innerHTML += `
        <option value="New Project">New Project</option>
        <option value="Instrument">Instrument</option>
        <option value="Electrical Assets">Electrical Assets</option>
        <option value="Other">Other</option>
      `;
    } else if (department === "Mechanical") {
      subCategoryDropdown.innerHTML += `
        <option value="Instruments">Instruments</option>
        <option value="Machines">Machines</option>
        <option value="Other">Other</option>
      `;
    }
  }



  function changeOptions(dropDownId, options) {
    var dropDown = document.querySelector(`#${dropDownId} .list`);
    var labels = dropDown.querySelectorAll("label.nested-dropdown");
    options.forEach(function(option, index) {
    labels[index].textContent = option;
    });
  }

  var input = document.querySelectorAll(".input-box");
  input.forEach(function(el) {
    el.onclick = function () {
    this.classList.toggle("open");
    let list = this.nextElementSibling;
    if (list.style.maxHeight) {
      list.style.maxHeight = null;
      list.style.boxShadow = null;
    } else {
      list.style.maxHeight = list.scrollHeight + "px";
      list.style.boxShadow =
      "0 1px 2px 0 rgba(0, 0, 0, 0.15),0 1px 3px 1px rgba(0, 0, 0, 0.1)";
    }
    };
  });

  var rad = document.querySelectorAll(".radio");
  rad.forEach((item) => {
    item.addEventListener("change", () => {
    var inputBox = item.parentNode.previousElementSibling;
    inputBox.innerHTML = item.nextElementSibling.innerHTML;
    inputBox.click();
    var nestedLists = document.querySelectorAll('.nested-list');
    nestedLists.forEach(function(list) {
      list.style.display = 'none';
    });
    });
  });

  var label = document.querySelectorAll("label");
  function search(searchin, dropdownId) {
    let searchVal = searchin.value;
    searchVal = searchVal.toUpperCase();
    let dropdown = document.querySelector(`#${dropdownId}`);
    let labels = dropdown.querySelectorAll("label");
    labels.forEach((item) => {
    let checkVal = item.textContent.toUpperCase();
    if (checkVal.indexOf(searchVal) == -1) {
      item.style.display = "none";
    } else {
      item.style.display = "flex";
    }
    let list = dropdown.querySelector(".list");
    list.style.maxHeight = list.scrollHeight + "px";
    });
  }


  function application1(){
    window.open("")
  }

  let poupup = document.getElementById("popup");

  function openPopup(){
    poupup.classList.add("open-popup")
  }

  function closePopup(){
    poupup.classList.remove("open-popup")
  }


  
  const allStar = document.querySelectorAll('.rating .star')
const ratingValue = document.querySelector('.rating input')

allStar.forEach((item, idx)=> {
	item.addEventListener('click', function () {
		let click = 0
		ratingValue.value = idx + 1

		allStar.forEach(i=> {
			i.classList.replace('bxs-star', 'bx-star')
			i.classList.remove('active')
		})
		for(let i=0; i<allStar.length; i++) {
			if(i <= idx) {
				allStar[i].classList.replace('bx-star', 'bxs-star')
				allStar[i].classList.add('active')
			} else {
				allStar[i].style.setProperty('--i', click)
				click++
			}
		}
	})
})