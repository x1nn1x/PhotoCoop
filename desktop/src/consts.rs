// PHOTOCOOP-HOOK: keep PhotoCoop data separate from official Graphite installs.
pub(crate) const APP_NAME: &str = "PhotoCoop";
#[cfg(any(target_os = "linux", target_os = "windows"))]
pub(crate) const APP_ID: &str = "dev.photocoop.PhotoCoop";

#[cfg(target_os = "linux")]
pub(crate) const APP_DIRECTORY_NAME: &str = "photocoop";
#[cfg(not(target_os = "linux"))]
pub(crate) const APP_DIRECTORY_NAME: &str = "PhotoCoop";
pub(crate) const APP_LOCK_FILE_NAME: &str = "instance.lock";
pub(crate) const APP_SOCKET_FILE_NAME: &str = "instance.sock";
pub(crate) const APP_STATE_FILE_NAME: &str = "state.ron";
pub(crate) const APP_PREFERENCES_FILE_NAME: &str = "preferences.ron";
pub(crate) const APP_DOCUMENTS_DIRECTORY_NAME: &str = "documents";
pub(crate) const APP_RESOURCES_DIRECTORY_NAME: &str = "resources";
