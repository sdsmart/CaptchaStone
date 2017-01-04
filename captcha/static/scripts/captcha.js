function handleClick(checkBox)
{
	if (checkBox.checked)
	{
		var height = $('#' + checkBox.value).height();
		document.getElementById(checkBox.value).style.opacity = '0.33';
		document.getElementById('div-' + checkBox.value).style.background = 'linear-gradient(to bottom, #12b83c ' + height.toString() + 'px, transparent 1px)'; //' + height.toString() + 'px)'; // 90px)';
	}
	else
	{
		document.getElementById(checkBox.value).style.opacity = '1.0';
		document.getElementById('div-' + checkBox.value).style.background = 'transparent';
	}
}