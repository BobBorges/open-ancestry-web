
window.onload = function() {
	var divsToHide = document.getElementsByClassName('initHide');
	for(var i = 0; i < divsToHide.length; i++){
         divsToHide[i].style.display = "none"; // depending on what you're doing
    }
}

function showHideDeets(target){
	var div = document.getElementById(target)
	var divSHer = document.getElementById(target + '_showerHider')
	if(div.style.display == 'none'){
		div.style.display = 'block';
		divSHer.innerHTML = "hide details&nbsp;<i class='fas fa-arrow-alt-circle-up'></i>"
	} else {
		div.style.display = 'none';
		divSHer.innerHTML = "show details&nbsp;<i class='fas fa-arrow-alt-circle-down'></i>"
	}
}

function showHideDeets1(target){
	var div = document.getElementById(target)
	var divSHer = document.getElementById(target + '_showerHider')
	if(div.style.display == 'none'){
		div.style.display = 'block';
		divSHer.innerHTML = "<i class='fas fa-arrow-alt-circle-up'></i>&nbsp;hide details"
	} else {
		div.style.display = 'none';
		divSHer.innerHTML = "<i class='fas fa-arrow-alt-circle-down'></i>&nbsp;show details"
	}
}

function showHideDeets2(target, container){
	var div = document.getElementById(target)
	var cont = document.getElementById(container)
	if(div.style.display == 'none'){
		div.style.display = 'block';
		cont.style.display = 'none';
	} else {
		div.style.display = 'none';
		cont.style.display = 'block';
	}
}


function showHideReplies(target) {
	// write this one for the reply section
	var div = document.getElementById(target);
	if (div.style.display == 'none'){
		div.style.display = 'block';
	} else {
		div.style.display = 'none';
	}
}

function showHideResearchForm() {
	var rfd = document.getElementById('research_form') 
	if(rfd.style.display == 'none') {
		rfd.style.display = 'block';
	} else {
		rfd.style.display = 'none';
	}
}


function personEditFormShowHide() {
	var pef = document.getElementById('person_edit_form')
	if(pef.style.display == 'none') {
		pef.style.display = 'block';
	} else {
		pef.style.display = 'none';
	}
}

function sourceEditFormShowHide() {
	var sef = document.getElementById('sourceEditForm')
	if(sef.style.display == 'none') {
		sef.style.display = 'block';
	} else {
		sef.style.display = 'none';
	}
}

function eventEditFormShowHide() {
	var edt = document.getElementById('edit_event_div')
	if (edt.style.display == 'none') {
		edt.style.display = 'block'
	} else {
		edt.style.display = 'none';
	}
}

function epochEditFormShowHide() {
	var edt = document.getElementById('edit_epoch_div')
	if (edt.style.display == 'none') {
		edt.style.display = 'block'
	} else {
		edt.style.display = 'none';
	}
}



function nuggetEditFormShowHide() {
	var edt = document.getElementById('edit_nugget_div')
	if (edt.style.display == 'none') {
		edt.style.display = 'block'
	} else {
		edt.style.display = 'none';
	}
}

function relationshipEditFormShowHide() {
	var edt = document.getElementById('edit_relationship_div')
	if (edt.style.display == 'none') {
		edt.style.display = 'block'
	} else {
		edt.style.display = 'none';
	}
}
function anShowHide(){
	var xyz = document.getElementById('alternative-name_add_div');
	if (xyz.style.display == 'none') {
		xyz.style.display = 'block'
	} else {
		xyz.style.display = 'none';
	}

}