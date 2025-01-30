package com.example.diff;

import com.intellij.openapi.actionSystem.AnAction;
import com.intellij.openapi.actionSystem.AnActionEvent;
import com.intellij.openapi.actionSystem.CommonDataKeys;
import com.intellij.openapi.command.WriteCommandAction;
import com.intellij.openapi.editor.Document;
import com.intellij.openapi.fileEditor.FileDocumentManager;
import com.intellij.openapi.project.Project;
import com.intellij.openapi.vfs.LocalFileSystem;
import com.intellij.openapi.vfs.VirtualFile;
import com.intellij.openapi.ui.Messages;
import org.jetbrains.annotations.NotNull;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.List;

public class PatchAction extends AnAction {
    private static final String BACKUP_SUFFIX = ".backup";
    private static final String PATCH_EXTENSION = ".patch";

    @Override
    public void actionPerformed(@NotNull AnActionEvent e) {
        Project project = e.getProject();
        if (project == null) return;

        // Try to get the file from the active editor first
        VirtualFile targetFile = e.getData(CommonDataKeys.VIRTUAL_FILE);
        if (targetFile == null) {
            com.intellij.psi.PsiFile psiFile = e.getData(CommonDataKeys.PSI_FILE);
            if (psiFile != null) {
                targetFile = psiFile.getVirtualFile();
            }
        }

        if (targetFile == null) {
            showError(project, "Please open a file to patch");
            return;
        }

        try {
            // Find first .patch file in the same directory
            VirtualFile parentDir = targetFile.getParent();
            VirtualFile patchFile = findPatchFileInDirectory(parentDir);

            if (patchFile == null) {
                showError(project, "No .patch file found in the same directory");
                return;
            }

            Path backupPath = Paths.get(targetFile.getPath() + BACKUP_SUFFIX);

            if (Files.exists(backupPath)) {
                revertChanges(project, targetFile, backupPath);
            } else {
                applyPatch(project, targetFile, patchFile, backupPath);
            }

        } catch (IOException ex) {
            showError(project, "Error: " + ex.getMessage());
        }
    }

    private VirtualFile findPatchFileInDirectory(VirtualFile dir) {
        if (dir == null) return null;

        VirtualFile[] children = dir.getChildren();
        for (VirtualFile child : children) {
            if (!child.isDirectory() && child.getName().endsWith(PATCH_EXTENSION)) {
                return child;
            }
        }
        return null;
    }

    private void applyPatch(Project project, VirtualFile targetFile, VirtualFile patchFile, Path backupPath)
            throws IOException {
        // Create backup
        Files.copy(Paths.get(targetFile.getPath()), backupPath);

        Document document = FileDocumentManager.getInstance().getDocument(targetFile);
        if (document == null) return;

        List<String> patchLines = Files.readAllLines(Paths.get(patchFile.getPath()));
        StringBuilder newContent = new StringBuilder();

        // Skip patch header lines
        boolean headerDone = false;
        for (String line : patchLines) {
            // Skip the patch header (lines starting with ---, +++, or @@)
            if (!headerDone) {
                if (line.startsWith("---") || line.startsWith("+++") || line.startsWith("@@")) {
                    continue;
                }
                headerDone = true;
            }

            // Process content lines
            if (line.startsWith("+")) {
                newContent.append(line.substring(1)).append("\n");
            }
        }

        WriteCommandAction.runWriteCommandAction(project, () ->
                document.setText(newContent.toString())
        );
    }

    private void revertChanges(Project project, VirtualFile targetFile, Path backupPath)
            throws IOException {
        Document document = FileDocumentManager.getInstance().getDocument(targetFile);
        if (document == null) return;

        String originalContent = new String(Files.readAllBytes(backupPath));

        WriteCommandAction.runWriteCommandAction(project, () ->
                document.setText(originalContent)
        );

        Files.delete(backupPath);
    }

    private void showError(Project project, String message) {
        Messages.showErrorDialog(project, message, "Patch Application Error");
    }

    @Override
    public void update(@NotNull AnActionEvent e) {
        // Enable the action if there's an open file
        VirtualFile file = e.getData(CommonDataKeys.VIRTUAL_FILE);
        if (file == null) {
            com.intellij.psi.PsiFile psiFile = e.getData(CommonDataKeys.PSI_FILE);
            if (psiFile != null) {
                file = psiFile.getVirtualFile();
            }
        }
        e.getPresentation().setEnabledAndVisible(file != null && !file.isDirectory());
    }
}

//package com.example.diff;
//
//import com.intellij.openapi.actionSystem.AnAction;
//import com.intellij.openapi.actionSystem.AnActionEvent;
//import com.intellij.openapi.actionSystem.CommonDataKeys;
//import com.intellij.openapi.command.WriteCommandAction;
//import com.intellij.openapi.editor.Document;
//import com.intellij.openapi.fileEditor.FileDocumentManager;
//import com.intellij.openapi.project.Project;
//import com.intellij.openapi.vfs.LocalFileSystem;
//import com.intellij.openapi.vfs.VirtualFile;
//import com.intellij.openapi.ui.Messages;
//import org.jetbrains.annotations.NotNull;
//
//import java.io.*;
//import java.nio.file.Files;
//import java.nio.file.Path;
//import java.nio.file.Paths;
//import java.util.List;
//
//public class PatchAction extends AnAction {
//    private static final String PATCH_FILENAME = "changes.patch";
//    private static final String TARGET_FILENAME = "target.txt";
//    private static final String BACKUP_SUFFIX = ".backup";
//
//    @Override
//    public void actionPerformed(@NotNull AnActionEvent e) {
//        Project project = e.getProject();
//        if (project == null) return;
//
//        VirtualFile projectDir = project.getBaseDir();
//        if (projectDir == null) return;
//
//        try {
//            VirtualFile targetFile = findFile(projectDir, TARGET_FILENAME);
//            if (targetFile == null) {
//                showError(project, "Target file not found: " + TARGET_FILENAME);
//                return;
//            }
//
//            Path backupPath = Paths.get(targetFile.getPath() + BACKUP_SUFFIX);
//
//            if (Files.exists(backupPath)) {
//                // Revert changes
//                revertChanges(project, targetFile, backupPath);
//            } else {
//                // Apply patch
//                VirtualFile patchFile = findFile(projectDir, PATCH_FILENAME);
//                if (patchFile == null) {
//                    showError(project, "Patch file not found: " + PATCH_FILENAME);
//                    return;
//                }
//                applyPatch(project, targetFile, patchFile, backupPath);
//            }
//
//        } catch (IOException ex) {
//            showError(project, "Error: " + ex.getMessage());
//        }
//    }
//
//    private void applyPatch(Project project, VirtualFile targetFile, VirtualFile patchFile, Path backupPath)
//            throws IOException {
//        // Create backup
//        Files.copy(Paths.get(targetFile.getPath()), backupPath);
//
//        Document document = FileDocumentManager.getInstance().getDocument(targetFile);
//        if (document == null) return;
//
//        List<String> patchLines = Files.readAllLines(Paths.get(patchFile.getPath()));
//        StringBuilder newContent = new StringBuilder();
//
//        // Simple patch application (you might want to use a proper patch library)
//        for (String line : patchLines) {
//            if (line.startsWith("+")) {
//                newContent.append(line.substring(1)).append("\n");
//            }
//        }
//
//        WriteCommandAction.runWriteCommandAction(project, () ->
//                document.setText(newContent.toString())
//        );
//    }
//
//    private void revertChanges(Project project, VirtualFile targetFile, Path backupPath)
//            throws IOException {
//        Document document = FileDocumentManager.getInstance().getDocument(targetFile);
//        if (document == null) return;
//
//        String originalContent = new String(Files.readAllBytes(backupPath));
//
//        WriteCommandAction.runWriteCommandAction(project, () ->
//                document.setText(originalContent)
//        );
//
//        Files.delete(backupPath);
//    }
//
//    private VirtualFile findFile(VirtualFile dir, String filename) {
//        return LocalFileSystem.getInstance().findFileByPath(
//                dir.getPath() + File.separator + filename
//        );
//    }
//
//    private void showError(Project project, String message) {
//        Messages.showErrorDialog(project, message, "Patch Application Error");
//    }
//
//    @Override
//    public void update(@NotNull AnActionEvent e) {
//        Project project = e.getProject();
//        e.getPresentation().setEnabledAndVisible(project != null);
//    }
//}