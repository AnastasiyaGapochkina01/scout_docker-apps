package main

import (
    "fmt"
    "log"
    "net/http"
    "sync/atomic"
)

var requestCount uint64
var running int32 = 1

func metricsHandler(w http.ResponseWriter, r *http.Request) {
    atomic.AddUint64(&requestCount, 1)
    fmt.Fprintf(w, "# HELP app_requests_total Total number of requests\n")
    fmt.Fprintf(w, "# TYPE app_requests_total counter\n")
    fmt.Fprintf(w, "app_requests_total %d\n", atomic.LoadUint64(&requestCount))
    fmt.Fprintf(w, "# HELP app_status Whether app is running (1=running)\n")
    fmt.Fprintf(w, "# TYPE app_status gauge\n")
    fmt.Fprintf(w, "app_status %d\n", running)
}

func mainHandler(w http.ResponseWriter, r *http.Request) {
    atomic.AddUint64(&requestCount, 1)
    fmt.Fprintf(w, "Welcome to the Go Metrics App!\n")
}

func adminHandler(w http.ResponseWriter, r *http.Request) {
    atomic.AddUint64(&requestCount, 1)
    if r.Method == "GET" {
        w.Header().Set("Content-Type", "text/html")
        fmt.Fprintf(w, `<html><body><form method="POST">Login: <input name="username"/><br>Password: <input type="password" name="password"/><br><input type="submit" value="Login"/></form></body></html>`)
        return
    }
    if err := r.ParseForm(); err != nil {
        http.Error(w, "Bad request", http.StatusBadRequest)
        return
    }
    username := r.FormValue("username")
    password := r.FormValue("password")
    if username == "admin" && password == "admin" {
        fmt.Fprintf(w, "Hello, admin!\n")
    } else {
        http.Error(w, "Unauthorized", http.StatusUnauthorized)
    }
}

func main() {
    http.HandleFunc("/metrics", metricsHandler)
    http.HandleFunc("/main", mainHandler)
    http.HandleFunc("/admin", adminHandler)

    log.Fatal(http.ListenAndServe("localhost:9113", nil))
}

