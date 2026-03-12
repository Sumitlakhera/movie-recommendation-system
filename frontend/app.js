const { useState, useRef, useEffect } = React;

const App = () => {
    const [movie, setMovie] = useState("");
    const [results, setResults] = useState([]);
    const [error, setError] = useState("");
    const [searchedMovie, setSearchedMovie] = useState(null);
    const [suggestions, setSuggestions] = useState([]);
    const [loading, setLoading] = useState(false);
    const [selectedMovie, setSelectedMovie] = useState(null);
    const [movieDetails, setMovieDetails] = useState(null);
    const [trending, setTrending] = useState([]);
    const [trendingLoading, setTrendingLoading] = useState(true);
    const [previewTrailer, setPreviewTrailer] = useState(null);
    const hoverTimer = useRef(null);
    const trendingRef = useRef(null);
    const inputRef = useRef(null);
    const trailerCache = useRef({});

    const API_BASE = "http://127.0.0.1:5000";

    useEffect(() => {

        fetch(`${API_BASE}/trending`)
            .then(res => res.json())
            .then(data => {
                setTrending(data);
                setTrendingLoading(false);
            })
            .catch(err => {

                setTrendingLoading(false);
            });
    }, []);

    const scrollTrendingLeft = () => {
        if (trendingRef.current) {
            trendingRef.current.scrollBy({
                left: -400,
                behavior: "smooth"
            });
        }
    };

    const scrollTrendingRight = () => {
        if (trendingRef.current) {
            trendingRef.current.scrollBy({
                left: 400,
                behavior: "smooth"
            });
        }
    };

    const handleSearch = () => {

        if (!movie) return;

        setLoading(true);
        setResults([]);
        setError("");

        fetch(`${API_BASE}/recommend?movie=${movie}`)
            .then((response) => response.json())
            .then((data) => {

                setLoading(false);

                if (data.error) {
                    setResults([]);
                    setSearchedMovie(null);
                    setError("No results found");
                } else {
                    setSearchedMovie(data.searched_movie);
                    setResults(data.recommendations);
                }

            })
            .catch((error) => {

                console.error(error);
                setLoading(false);
                setResults([]);
                setError("Something went wrong");

            });
    };

    const trendingItems = trendingLoading
        ? Array.from({ length: 8 }, () => ({ skeleton: true }))
        : trending;


    const formatRuntime = (minutes) => {

        if (!minutes) return "";

        const hours = Math.floor(minutes / 60);
        const mins = minutes % 60;

        return `${hours}h ${mins}m`;
    };

    return React.createElement(
        "div",
        { className: "container" },

        React.createElement(
            "div",
            { className: "hero" },

            React.createElement("h1", { className: "hero-title" }, "Discover Your Next Movie"),

            React.createElement(
                "p",
                { className: "hero-subtitle" },
                "Search a movie and get AI-powered recommendations instantly"
            )
        ),

        error && React.createElement("div", { className: "error-message" }, error),

        React.createElement(
            "div",
            { className: "search-container" },

            React.createElement(
                "div",
                { className: "search-row" },

                React.createElement(
                    "div",
                    { className: "search-box" },

                    React.createElement("input", {
                        ref: inputRef,
                        className: "search-bar",
                        placeholder: "Enter movie name...",
                        value: movie,
                        onKeyDown: (e) => {

                            if (e.key === "Enter") {
                                handleSearch();
                            }
                        },
                        onChange: (e) => {
                            const value = e.target.value;
                            setMovie(value);

                            if (value.length === 0) {
                                setSuggestions([]);
                                return;
                            }

                            fetch(`${API_BASE}/search?query=${value}`)
                                .then((res) => res.json())
                                .then((data) => setSuggestions(data));
                        },
                    }),

                    React.createElement(
                        "div",
                        { className: "suggestions" },

                        suggestions.map((title, index) =>
                            React.createElement(
                                "div",
                                {
                                    key: index,
                                    className: "suggestion-item",
                                    onClick: () => {
                                        setMovie(title);
                                        setSuggestions([]);
                                        if (inputRef.current) {
                                            inputRef.current.focus();
                                        }
                                    },
                                },
                                title
                            )
                        )
                    )
                ),

                React.createElement(
                    "button",
                    {
                        className: "button",
                        onClick: handleSearch
                    },
                    "Recommend"
                )
            ),
        ),

        (trendingLoading || trending.length > 0) &&
        React.createElement(
            "div",
            null,

            React.createElement(
                "div",
                { className: "section-title" },
                "Trending Movies"
            ),

            React.createElement(
                "div",
                { className: "trending-wrapper" },

                React.createElement("div", { className: "fade-left" }),

                React.createElement(
                    "button",
                    { className: "scroll-btn left", onClick: scrollTrendingLeft },
                    "❮"
                ),

                React.createElement(
                    "div",
                    { className: "trending-row", ref: trendingRef },

                    trendingItems.map((movie, index) =>
                        React.createElement(
                            "div",
                            {
                                key: index,
                                className: "movie-card",

                                onClick: () => {

                                    if (movie.skeleton) return;

                                    fetch(`${API_BASE}/movie-details?id=${movie.movie_id}`)
                                        .then(res => res.json())
                                        .then(data => {
                                            setPreviewTrailer(null);
                                            setMovieDetails(data);
                                            setSelectedMovie(movie);
                                        });

                                },

                                onMouseEnter: () => {
                                    clearTimeout(hoverTimer.current);

                                    if (movie.skeleton) return;

                                    hoverTimer.current = setTimeout(() => {

                                        const cachedTrailer = trailerCache.current[movie.movie_id];
                                        if (cachedTrailer) {

                                            setPreviewTrailer({
                                                id: movie.movie_id,
                                                url: cachedTrailer
                                            });

                                        } else {

                                            fetch(`${API_BASE}/trailer?id=${movie.movie_id}`)
                                                .then(res => res.json())
                                                .then(data => {

                                                    if (data.trailer) {

                                                        trailerCache.current[movie.movie_id] = data.trailer;

                                                        setPreviewTrailer({
                                                            id: movie.movie_id,
                                                            url: data.trailer
                                                        });

                                                    }

                                                });

                                        }

                                    }, 3000);
                                },

                                onMouseLeave: () => {

                                    clearTimeout(hoverTimer.current);
                                    setPreviewTrailer(null);
                                }
                            },

                            movie.skeleton
                                ? React.createElement("div", { className: "poster skeleton-card" })

                                : previewTrailer && previewTrailer.id === movie.movie_id

                                    ? React.createElement("iframe", {
                                        src: previewTrailer.url,
                                        className: "poster",
                                        frameBorder: "0",
                                        allow: "autoplay",
                                        allowFullScreen: false,
                                        loading: "lazy"
                                    })

                                    : React.createElement("img", {
                                        src: movie.poster
                                            ? movie.poster
                                            : "https://dummyimage.com/300x450/222/fff&text=No+Poster",
                                        className: "poster"
                                    }),

                            !movie.skeleton &&
                            React.createElement(
                                "div",
                                { className: "movie-title" },
                                movie.title
                            )
                        )
                    )

                ),

                React.createElement(
                    "button",
                    { className: "scroll-btn right", onClick: scrollTrendingRight },
                    "❯"
                ),

                React.createElement("div", { className: "fade-right" })
            ),
        ),

        searchedMovie &&
        React.createElement(
            "div",
            { className: "searched-movie-hero" },

            React.createElement("img", {
                src: searchedMovie.poster,
                className: "hero-poster"
            }),

            React.createElement(
                "div",
                { className: "hero-info" },

                React.createElement(
                    "h2",
                    { className: "hero-title" },
                    searchedMovie.title
                ),

                React.createElement(
                    "p",
                    { className: "hero-meta" },
                    `${searchedMovie.genres?.join(", ")} • ${formatRuntime(searchedMovie.runtime)}`
                ),

                searchedMovie.tagline &&
                React.createElement(
                    "p",
                    { className: "hero-tagline" },
                    searchedMovie.tagline
                ),

                React.createElement(
                    "p",
                    { className: "hero-overview" },
                    searchedMovie.overview
                )
            )
        ),


        results.length > 0 &&
        React.createElement(
            "div",
            { className: "section-title" },
            "Recommended Movies"
        ),

        loading
            ? React.createElement(
                "div",
                { className: "movies-grid" },
                Array.from({ length: 5 }).map((_, index) =>

                    React.createElement(
                        "div",
                        {
                            key: index,
                            className: "movie-card"
                        },
                        React.createElement("div", {
                            key: index,
                            className: "poster skeleton-card"
                        })
                    )
                ))
            : React.createElement(
                "div",
                { className: "movies-grid" },

                results.map((movie, index) =>
                    React.createElement(
                        "div",
                        {
                            className: "movie-card",
                            key: index,
                            onClick: () => {
                                fetch(`${API_BASE}/movie-details?id=${movie.movie_id}`)
                                    .then(res => res.json())
                                    .then(data => {
                                        setMovieDetails(data)
                                        setSelectedMovie(movie);
                                    })
                            }
                        },

                        React.createElement("img", {
                            src: movie.poster
                                ? movie.poster
                                : "https://dummyimage.com/300x450/222/fff&text=No+Poster+Available",
                            className: "poster",
                            onError: (e) => {
                                e.target.onerror = null;
                                e.target.src =
                                    "https://dummyimage.com/300x450/222/fff&text=No+Poster+Available";
                            }
                        }),

                        React.createElement("div", { className: "movie-title" }, movie.title)
                    )
                )
            ),


        selectedMovie &&
        React.createElement(
            "div",
            {
                className: "modal-overlay",
                onClick: () => setSelectedMovie(null)
            },

            React.createElement(
                "div",
                {
                    className: "modal-content",
                    onClick: (e) => e.stopPropagation()
                },

                React.createElement("img", {
                    src: selectedMovie.poster || "./no-poster.png",
                    className: "modal-poster"
                }),

                React.createElement(
                    "div",
                    { className: "modal-info" },

                    React.createElement(
                        "h2",
                        null,
                        movieDetails ? movieDetails.title : selectedMovie.title
                    ),

                    movieDetails &&
                    React.createElement(
                        "p",
                        null,
                        movieDetails.overview
                    ),

                    movieDetails &&
                    React.createElement(
                        "p",
                        null,
                        "Release: " + movieDetails.release_date
                    ),

                    movieDetails &&
                    React.createElement(
                        "p",
                        null,
                        "Rating: " + movieDetails.rating
                    ),

                    React.createElement(
                        "button",
                        {
                            className: "close-button",
                            onClick: () => {
                                setSelectedMovie(null);
                                setMovieDetails(null);
                            }
                        },
                        "Close"
                    )
                )
            )
        )

    );
};

ReactDOM.render(React.createElement(App), document.getElementById("root"));
