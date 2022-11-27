function deleteNote(predId) {
  var result = confirm("Are you sure you want to delete this prediction?");
  if (result) {
    fetch("/delete-pred", {
      method: "POST",
      body: JSON.stringify({ predID: predId }),
    }).then((_res) => {
      window.location.href = "/dashboard";
    });
  }
}

function deleteReview(userId) {
  var result = confirm("Are you sure you want to delete your review?");
  if (result) {
    fetch("/delete-review", {
      method: "POST",
      body: JSON.stringify({ userID: userId }),
    }).then((_res) => {
      window.location.href = "/dashboard";
    });
  }
}
