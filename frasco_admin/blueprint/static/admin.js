/**
 * globals
 */
var MOBILE_VIEW = 992;

$(function() {
    'use strict';

    function getWidth() {
      return window.innerWidth;
    }

    if (typeof(localStorage) == 'undefined') {
        // provide mock localStorage object for dumb browsers
        localStorage = {
            setItem: function(key, value) {},
            getItem: function(key) { return null; }
        };
    }

    var App = {
        /**
         * init
         */
        init: function() {
            this.cacheElements();
            this.bindEvents();
            this.checkViewport();
        },

        /**
         * cache elements
         */
        cacheElements: function() {
            this.$viewport    = $(window);
            this.$pageWrapper = $("#page-wrapper");
            this.$toggleBtn   = $("#toggle-sidebar");
        },

        /**
         * bind events to elements
         */
        bindEvents: function() {
            this.$viewport.on('resize', this.viewportResize.bind(this));
            this.$toggleBtn.on('click', this.toggleSidebar.bind(this));
        },

        /**
         * trigger checkviewport on resize
         */
        viewportResize: function() {
            this.checkViewport();
        },

        /**
         * toggles sidebar
         */
        toggleSidebar: function(e) {
            this.$pageWrapper.toggleClass('active');
            localStorage.setItem('admin-sidebar-visible', this.$pageWrapper.hasClass("active"));
        },

        /**
         * Checks the viewport and toggles sidebar if toggled
         */
        checkViewport: function() {
            if (getWidth() >= MOBILE_VIEW) {
                var visible = localStorage.getItem('admin-sidebar-visible');
                if (visible === null) {
                    this.$pageWrapper.addClass("active");
                } else {
                    if(visible === "true") {
                        this.$pageWrapper.addClass("active");
                    } else {
                        this.$pageWrapper.removeClass("active");
                    }
                }
            } else {
                this.$pageWrapper.removeClass("active");
            }
        },

    };

    App.init();

});