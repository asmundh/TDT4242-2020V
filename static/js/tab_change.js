$('#project-toggle a[data-toggle="list"]').on('shown.bs.tab', function (e) {
  if (e.relatedTarget) {
    $('#'+e.relatedTarget.id).removeClass('active') // previous active tab
  }
})
