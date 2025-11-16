import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  query: string = '';
  results: string[] = [];
  loading: boolean = false;
  error: string | null = null;

  onSearch() {
    if (!this.query.trim()) {
      this.error = 'Please enter a company name.';
      this.results = [];
      return;
    }

    this.error = null;
    this.loading = true;
    this.results = [];

    // Simulate a fake search (e.g., API call)
    setTimeout(() => {
      this.results = [
        `${this.query} stock rises after positive news.`,
        `${this.query} announces major product update.`,
        `${this.query} faces new competition in market.`
      ];
      this.loading = false;
    }, 1000);
  }
}
