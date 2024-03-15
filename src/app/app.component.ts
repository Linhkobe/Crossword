import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  handleFileUpload(file: File): void {
    // Here, you implement the code to send the image to the server
    // and receive the crossword puzzle resolution.
    console.log("Image sent:", file.name);
    // Simulate a response
    setTimeout(() => {
      document.getElementById('crossword-result')!.textContent = "Simulated crossword puzzle resolution...";
    }, 1500);
  }

  sendAlerte(): void {
    const inputFile = document.getElementById('crossword-image-input') as HTMLInputElement;
    if (inputFile.files && inputFile.files.length > 0) {
      const file = inputFile.files[0];
      this.handleFileUpload(file);
    } else {
      alert("Veuillez sélectionner une image.");
    }
  }
}
