var progress = { percentage : 12 }

Vue.component('progress-text', {
	template: "<span>{{ percentage }}</span>",
	data: function () {
		return progress
	}
})

new Vue({
	el : '#app'
})