// This File defines vue reactivity for the index page

let app = {};

let init = (app) => {
    
    app.data = {

        // bools for toggling what html to display
        feed_mode:  true,
        add_mode:   false,
        view_mode:  false,

        // feed variables
        feed:       [],

        // add_story variables
        add_title:      "",
        add_content:    "",
        add_author:     "",

        // view_story variables
        view_title:     "",
        view_content:   "",
        view_author:    "",
        view_date:      "",

    };
    
    app.enumerate = (a) => { // This adds an _idx field to each element in a.
        let k = 0;
        a.map((e) => {e._idx = k++;});
        return a;
    };

    app.set_feed_mode = () => {
        app.vue.view_mode   = false;
        app.vue.add_mode    = false;
        app.vue.feed_mode   = true;
    }

    app.set_add_mode = () => {
        app.vue.feed_mode   = false;
        app.vue.view_mode   = false;
        app.vue.add_mode    = true;
    }

    app.set_view_mode = () => {
        app.vue.feed_mode = false;
        app.vue.add_mode  = false;
        app.vue.view_mode = true;
    }

    app.view = (_idx) => {
        console.log("view", _idx);
        app.vue.view_title      = app.vue.feed[_idx].title;
        app.vue.view_content    = app.vue.feed[_idx].content;
        app.vue.view_author     = app.vue.feed[_idx].author;
        app.vue.view_date       = app.vue.feed[_idx].creation_date;
        console.log(app.vue.view_title);
        view_date_c     = "time";

        app.set_view_mode();
    }

    app.add_story = () => {
        axios.post(add_story_url, {
            title:      app.data.add_title,
            content:    app.data.add_content,
            author:     app.data.add_author,
        }).then((r) => {
            console.log("story added");
            app.refresh(); // only really need the id for the new story
            app.vue.add_mode  = false;
            app.vue.feed_mode = true;

        })
    };

    app.refresh = () => {
        axios.get(get_feed_url).then((r) => {
            app.vue.feed = app.enumerate(r.data.feed);
            console.log(r.data.feed);
            console.log("Feed Re-Loaded");
        });
    }
    
    app.methods = {
        set_feed_mode:  app.set_feed_mode,
        set_add_mode:   app.set_add_mode,
        set_view_mode:  app.set_view_mode,

        view:           app.view,
        add_story:      app.add_story,
        refresh:        app.refresh,
    };
    
    app.vue = new Vue({
        el:      "#vue-target",
        data:    app.data,
        methods: app.methods,
    });
    
    app.init = () => {
        console.log("index.js Loaded");
        axios.get(get_feed_url).then((r) => {
            app.vue.feed = app.enumerate(r.data.feed);
            console.log(r.data.feed);
            console.log("Feed Loaded");
        });
    };

    app.init();
};

init(app);
