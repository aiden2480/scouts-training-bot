var token = document.querySelector("meta[name=csrf-token]").content;
var video = document.querySelector('video[id="' + arguments[0] + '"]');
var data = new FormData();

data.append("object_id", arguments[0]);
data.append("learning_module_id", arguments[0]);
data.append("last_completed_at", new Date().toString());
data.append("current_progress", video.duration);

fetch("https://training.scouts.com.au/learning_object_members/set_completion?learning_object_member_id=", {
    body: new URLSearchParams(data),
    method: "post",
    headers: {
        "X-Csrf-Token": token,
    },
}).then((resp) => {
    document.querySelector("a.btn-close").click();
});
