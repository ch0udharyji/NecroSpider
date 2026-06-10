use inquire::{Select, Confirm, ui::{RenderConfig, Color as InquireColor, StyleSheet, Styled}};
use std::process::{Command, Stdio};
use std::io::{self, BufRead, BufReader};
use std::thread;
use std::time::Duration;
use std::path::Path;
use std::fs::File;
use indicatif::{ProgressBar, ProgressStyle};
use crossterm::{
    execute,
    terminal::{Clear, ClearType},
    cursor::MoveTo,
    style::{Color, Print, ResetColor, SetForegroundColor, Attribute, SetAttribute},
};

fn get_render_config() -> RenderConfig {
    let mut render_config = RenderConfig::default();
    render_config.prompt_prefix = Styled::new("?").with_fg(InquireColor::DarkRed);
    render_config.highlighted_option_prefix = Styled::new("▶").with_fg(InquireColor::DarkRed);
    render_config.selected_checkbox = Styled::new("◉").with_fg(InquireColor::DarkRed);
    render_config.scroll_up_prefix = Styled::new("▲");
    render_config.scroll_down_prefix = Styled::new("▼");
    render_config.answer = StyleSheet::new().with_fg(InquireColor::DarkRed);
    render_config
}

fn splash_screen() {
    let mut stdout = io::stdout();
    execute!(stdout, Clear(ClearType::All), MoveTo(0, 0)).unwrap();
    
    let splash = r#"
    ███╗   ██╗███████╗██████╗ ██████╗  ██████╗ ███████╗██████╗ ██╗██████╗ ███████╗██████╗ 
    ████╗  ██║██╔════╝██╔════╝ ██╔══██╗██╔═══██╗██╔════╝██╔══██╗██║██╔══██╗██╔════╝██╔══██╗
    ██╔██╗ ██║█████╗  ██║      ██████╔╝██║   ██║███████╗██████╔╝██║██║  ██║█████╗  ██████╔╝
    ██║╚██╗██║██╔══╝  ██║      ██╔══██╗██║   ██║╚════██║██╔═══╝ ██║██║  ██║██╔══╝  ██╔══██╗
    ██║ ╚████║███████╗╚██████╗ ██║  ██║╚██████╔╝███████║██║     ██║██████╔╝███████╗██║  ██║
    ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝     ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝
    "#;
    
    execute!(
        stdout,
        SetForegroundColor(Color::DarkRed),
        SetAttribute(Attribute::Bold),
        Print(splash),
        ResetColor,
        Print("\n\n"),
        SetForegroundColor(Color::White),
        Print("                                     by -> ch0udharyji\n\n"),
        ResetColor
    ).unwrap();
    
    thread::sleep(Duration::from_millis(1500));
}

fn run_installation_task(cmd: &mut Command, task_name: &str) -> bool {
    let spinner = ProgressBar::new_spinner();
    spinner.set_style(
        ProgressStyle::default_spinner()
            .tick_chars("⠁⠂⠄⡀⢀⠠⠐⠈ ")
            .template("{spinner:.red} {msg}")
            .unwrap()
    );
    spinner.enable_steady_tick(Duration::from_millis(80));
    spinner.set_message(format!("\x1b[1m\x1b[31m{}\x1b[0m Starting...", task_name));

    cmd.stdout(Stdio::piped());
    cmd.stderr(Stdio::piped());
    
    let mut child = match cmd.spawn() {
        Ok(child) => child,
        Err(e) => {
            spinner.finish_with_message(format!("\x1b[31m✖ Failed:\x1b[0m {} ({})", task_name, e));
            return false;
        }
    };

    let stdout = child.stdout.take().unwrap();
    let stderr = child.stderr.take().unwrap();

    let spinner_clone = spinner.clone();
    let task_name_clone = task_name.to_string();
    let stdout_thread = thread::spawn(move || {
        let reader = BufReader::new(stdout);
        for line in reader.lines() {
            if let Ok(l) = line {
                let short_line: String = l.chars().take(60).collect();
                spinner_clone.set_message(format!("\x1b[1m\x1b[31m{}\x1b[0m \x1b[90m{}\x1b[0m", task_name_clone, short_line));
            }
        }
    });

    let spinner_clone2 = spinner.clone();
    let task_name_clone2 = task_name.to_string();
    let stderr_thread = thread::spawn(move || {
        let reader = BufReader::new(stderr);
        for line in reader.lines() {
            if let Ok(l) = line {
                let short_line: String = l.chars().take(60).collect();
                spinner_clone2.set_message(format!("\x1b[1m\x1b[31m{}\x1b[0m \x1b[33m{}\x1b[0m", task_name_clone2, short_line));
            }
        }
    });

    stdout_thread.join().unwrap();
    stderr_thread.join().unwrap();

    let status = child.wait().unwrap();
    if status.success() {
        spinner.finish_with_message(format!("\x1b[32m✔ Completed:\x1b[0m \x1b[1m{}\x1b[0m", task_name));
        true
    } else {
        spinner.finish_with_message(format!("\x1b[31m✖ Failed:\x1b[0m \x1b[1m{}\x1b[0m", task_name));
        false
    }
}

fn check_and_install_python() {
    let python_check = Command::new("python3").arg("--version").output();
    if python_check.is_err() || !python_check.unwrap().status.success() {
        println!("  \x1b[33m[!] Python3 is not installed. Initiating setup...\x1b[0m");
        let mut cmd = Command::new("sudo");
        cmd.args(["apt-get", "update"]);
        run_installation_task(&mut cmd, "System Repositories");
        
        let mut cmd2 = Command::new("sudo");
        cmd2.args(["apt-get", "install", "-y", "python3", "python3-pip", "python3-venv"]);
        run_installation_task(&mut cmd2, "Python3 & Pip");
    }
}

fn check_and_install_docker() {
    let docker_check = Command::new("docker").arg("--version").output();
    if docker_check.is_err() || !docker_check.unwrap().status.success() {
        println!("  \x1b[33m[!] Docker is not installed. Initiating setup...\x1b[0m");
        let mut cmd = Command::new("sh");
        cmd.args(["-c", "curl -fsSL https://get.docker.com | sudo sh"]);
        run_installation_task(&mut cmd, "Docker Daemon");
    }
}

fn get_necrospider_dir() -> String {
    if Path::new("../sf.py").exists() {
        if let Ok(path) = std::fs::canonicalize("..") {
            return path.to_string_lossy().into_owned();
        }
    }
    let home = std::env::var("HOME").expect("Could not find HOME environment variable");
    format!("{}/.necrospider-app", home)
}

fn ensure_repo_ready() -> String {
    let repo_dir = get_necrospider_dir();
    let git_dir = format!("{}/.git", repo_dir);
    
    if !Path::new(&repo_dir).exists() || !Path::new(&git_dir).exists() {
        if !Path::new(&repo_dir).exists() {
            println!("  \x1b[33m[!] NecroSpider not found locally. Initiating clone...\x1b[0m");
        } else {
            println!("  \x1b[33m[!] Invalid repository found. Re-cloning...\x1b[0m");
            let _ = std::fs::remove_dir_all(&repo_dir);
        }
        let mut cmd = Command::new("git");
        cmd.args(["clone", "https://github.com/ch0udharyji/NecroSpider.git", &repo_dir]);
        run_installation_task(&mut cmd, "Cloning Repository");
    } else {
        println!("  \x1b[90mChecking for updates...\x1b[0m");
        let mut pull_cmd = Command::new("git");
        pull_cmd.current_dir(&repo_dir);
        pull_cmd.args(["pull"]);
        if let Ok(output) = pull_cmd.output() {
            let stdout = String::from_utf8_lossy(&output.stdout);
            if output.status.success() && !stdout.contains("Already up to date.") {
                println!("  \x1b[32m✔ NecroSpider has been updated successfully.\x1b[0m");
                let _ = std::fs::remove_file(format!("{}/.python_deps_installed", repo_dir));
                let _ = std::fs::remove_file(format!("{}/.docker_img_built", repo_dir));
            }
        }
    }
    repo_dir
}

fn spawn_server(mut cmd: Command, mode: &str) {
    cmd.stdout(Stdio::null());
    cmd.stderr(Stdio::null());
    cmd.stdin(Stdio::null());
    
    let mut child = match cmd.spawn() {
        Ok(c) => c,
        Err(e) => {
            println!("[\x1b[31m!\x1b[0m] Failed to start server: {}", e);
            return;
        }
    };

    thread::sleep(Duration::from_secs(3));

    let mut stdout = io::stdout();
    execute!(stdout, Clear(ClearType::All), MoveTo(0, 0)).unwrap();
    
    println!("\x1b[31m╔════════════════════════════════════════════════════════════╗\x1b[0m");
    println!("\x1b[31m║\x1b[0m               \x1b[1m\x1b[37mNECROSPIDER SERVER IS ONLINE\x1b[0m                 \x1b[31m║\x1b[0m");
    println!("\x1b[31m╠════════════════════════════════════════════════════════════╣\x1b[0m");
    println!("\x1b[31m║\x1b[0m \x1b[90mMode:\x1b[0m       {:<46} \x1b[31m║\x1b[0m", mode);
    println!("\x1b[31m║\x1b[0m \x1b[90mAddress:\x1b[0m    \x1b[34m{:<46}\x1b[0m \x1b[31m║\x1b[0m", "http://127.0.0.1:5001");
    println!("\x1b[31m╚════════════════════════════════════════════════════════════╝\x1b[0m\n");
    
    loop {
        let options = vec!["Launch Browser Dashboard", "Shutdown Server"];
        let ans = Select::new("Action:", options.clone())
            .with_render_config(get_render_config())
            .prompt();
        
        match ans {
            Ok(choice) => {
                if choice == options[0] {
                    let mut browser_cmd = Command::new("python3");
                    browser_cmd.args(["-m", "webbrowser", "http://127.0.0.1:5001"]);
                    browser_cmd.stdout(Stdio::null());
                    browser_cmd.stderr(Stdio::null());
                    browser_cmd.stdin(Stdio::null());
                    let _ = browser_cmd.spawn();
                } else if choice == options[1] {
                    println!("\n  \x1b[90mInitiating shutdown sequence...\x1b[0m");
                    let _ = child.kill();
                    let _ = child.wait();
                    println!("  \x1b[31mServer offline.\x1b[0m\n");
                    break;
                }
            }
            Err(_) => {
                let _ = child.kill();
                break;
            }
        }
    }
}

fn run_python_mode() {
    let repo_dir = ensure_repo_ready();
    let marker_file = format!("{}/.python_deps_installed", repo_dir);
    if !Path::new(&marker_file).exists() {
        check_and_install_python();
        
        let mut pip_cmd = Command::new("pip3");
        let req_file = format!("{}/requirements.txt", repo_dir);
        pip_cmd.args(["install", "-r", &req_file, "--break-system-packages"]);
        if run_installation_task(&mut pip_cmd, "Python Packages") {
            let mut npm_cmd = Command::new("npm");
            npm_cmd.current_dir(format!("{}/necrospider/static", repo_dir));
            npm_cmd.args(["install"]);
            let _ = run_installation_task(&mut npm_cmd, "Web UI Assets");
            
            let _ = File::create(marker_file);
        }
    }

    let mut sf_cmd = Command::new("python3");
    sf_cmd.current_dir(&repo_dir);
    sf_cmd.args(["sf.py", "-l", "127.0.0.1:5001"]);
    
    spawn_server(sf_cmd, "Python (Local)");
}

fn run_docker_mode() {
    let repo_dir = ensure_repo_ready();
    let marker_file = format!("{}/.docker_img_built", repo_dir);
    if !Path::new(&marker_file).exists() {
        check_and_install_docker();
        
        let mut build_cmd = Command::new("sudo");
        build_cmd.args(["docker", "build", "-t", "necrospider", &repo_dir]);
        if run_installation_task(&mut build_cmd, "Docker Image Build") {
            let _ = File::create(marker_file);
        }
    }

    let mut run_cmd = Command::new("sudo");
    run_cmd.current_dir(&repo_dir);
    run_cmd.args(["docker", "run", "--rm", "-p", "5001:5001", "necrospider"]);
    
    spawn_server(run_cmd, "Docker Container");
}

fn run_uninstall() {
    let ans = Confirm::new("Are you sure you want to completely uninstall NecroSpider and delete all data?")
        .with_default(false)
        .prompt();

    match ans {
        Ok(true) => {
            println!("\n  \x1b[31m[!] Initiating total uninstallation...\x1b[0m");
            
            let home = std::env::var("HOME").expect("Could not find HOME environment variable");
            
            let paths_to_remove = vec![
                format!("{}/.necrospider", home),
                format!("{}/.necrospider-app", home),
                format!("{}/.necrospider_history", home),
            ];

            for p in paths_to_remove {
                let path = Path::new(&p);
                if path.exists() {
                    println!("  \x1b[90mRemoving {}\x1b[0m", p);
                    if path.is_dir() {
                        let _ = std::fs::remove_dir_all(path);
                    } else {
                        let _ = std::fs::remove_file(path);
                    }
                }
            }

            println!("  \x1b[90mRemoving Docker image (if exists)...\x1b[0m");
            let mut docker_cmd = Command::new("sudo");
            docker_cmd.args(["docker", "rmi", "-f", "necrospider"]);
            docker_cmd.stdout(Stdio::null());
            docker_cmd.stderr(Stdio::null());
            let _ = docker_cmd.status();

            println!("  \x1b[32m✔ Uninstallation complete.\x1b[0m");
            println!("  \x1b[90mNote: You can remove the CLI itself by running `cargo uninstall necrospider-cli`.\x1b[0m\n");
        }
        _ => {
            println!("  \x1b[33mUninstallation cancelled.\x1b[0m");
        }
    }
}

fn main() {
    splash_screen();

    let options = vec!["Python (Local)", "Docker", "Uninstall"];
    
    let ans = Select::new("Engine:", options.clone())
        .with_render_config(get_render_config())
        .prompt();

    match ans {
        Ok(choice) => {
            if choice == "Python (Local)" {
                run_python_mode();
            } else if choice == "Docker" {
                run_docker_mode();
            } else if choice == "Uninstall" {
                run_uninstall();
            }
        }
        Err(_) => println!("  \x1b[31m[!] Terminated.\x1b[0m"),
    }
}
