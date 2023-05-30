// This File defines vue reactivity for the index page

let app = {}; // Main Vue Obj

let init = (app) => { // Vue Stuff

    app.data = { // Vue data
        new_story: [],
        add_title: "",
        add_content: "",
        add_author: "",
    };

    app.enumerate = (a) => { // This adds an _idx field to each element in a.
        let k = 0;
        a.map((e) => { e._idx = k++; });
        return a;
    };

    app.add_story = () => {
        axios.post(add_story_url, {
            title:      app.data.add_title,
            content:    app.data.add_content,
            author:     app.data.add_author,
        }).then((r) => {
            console.log(r.data)
        })
    };

    app.methods = {add_story: app.add_story,};

    app.vue = new Vue({ // This creates the Vue instance.
        el: "#vue-target",
        data: app.data,
        methods: app.methods,
    });

    app.init = () => { // And this initializes it.
        console.log("add_story vue.js started");
    };

    app.init(); // Call to the initializer.
};

init(app); // This takes the (empty) app object, and initializes it.
