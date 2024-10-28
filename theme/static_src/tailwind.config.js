/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        "../templates/**/*.html",

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        "../../templates/**/*.html",

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        "../../**/templates/**/*.html",

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    theme: {
        extend: {},
    },
    daisyui: {
        themes: [
            {
                "my-light": {
                    primary: "#f26b76",
                    "primary-focus": "#f2776b",
                    "primary-content": "#000000",

                    secondary: "#f2976b",
                    "secondary-focus": "#f2ae68",
                    "secondary-content": "#000000",

                    accent: "#f26bc8",
                    "accent-focus": "#f2b4bb",
                    "accent-content": "#000000",

                    neutral: "#333c4d",
                    "neutral-focus": "#1f242e",
                    "neutral-content": "#f9fafb",

                    "base-100": "#ffffff",
                    "base-200": "#e3e6e8",
                    "base-300": "#d4d4d4",
                    "base-content": "#333c4d",

                    info: "#1c92f2",
                    success: "#009485",
                    warning: "#ff9900",
                    error: "#ff5724",

                    "--rounded-box": "1rem",
                    "--rounded-btn": ".5rem",
                    "--rounded-badge": "1.9rem",

                    "--animation-btn": "0",
                    "--animation-input": "0",

                    "--btn-text-case": "uppercase",
                    "--navbar-padding": ".5rem",
                    "--border-btn": "1px",
                },
            },
            {
                "my-dark": {
                    primary: "#55a548",
                    "primary-focus": "#376a2f",
                    "primary-content": "#ffffff",

                    secondary: "#4da6db",
                    "secondary-focus": "#2ca2db",
                    "secondary-content": "#ffffff",

                    accent: "#d6b56b",
                    "accent-focus": "#e3f080",
                    "accent-content": "#ffffff",

                    neutral: "#2a2a37",
                    "neutral-focus": "#16181d",
                    "neutral-content": "#ffffff",

                    "base-100": "#282c34",
                    "base-200": "#1f2228",
                    "base-300": "#16181d",
                    "base-content": "#ebecf0",

                    info: "#38b6ff",
                    success: "#7bc828",
                    warning: "#dbac48",
                    error: "#ff4d4d",

                    "--rounded-box": "1.5rem",
                    "--rounded-btn": "1.5rem",
                    "--rounded-badge": "1.5rem",

                    "--animation-btn": ".25s",
                    "--animation-input": ".2s",

                    "--btn-text-case": "uppercase",
                    "--navbar-padding": ".5rem",
                    "--border-btn": "1.5px",
                },
            },
        ],
        darkTheme: "my-dark",
        base: true,
        styled: true,
        prefix: "",
        logs: true,
        themeRoot: ":root",
    },
    plugins: [require("daisyui")],
};
