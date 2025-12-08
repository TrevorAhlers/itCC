import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { ChangeDetectorRef } from '@angular/core';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, FormsModule,HttpClientModule],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})

export class HomeComponent {
  query: string = '';
  results: string[] = [];
  loading: boolean = false;
  error: string | null = null;
  stockData: any = null;

  constructor(private http: HttpClient, private cd: ChangeDetectorRef) {}

  exportCSV() {
  const url = 'http://localhost:5000/export_csv';
  window.open(url, '_blank'); // opens the CSV file in a new tab for download
 }

  onSearch() {
    if (!this.query.trim()) {
      this.error = 'Please enter a company name.';
      this.results = [];
      return;
    }

    

    this.error = null;
    this.loading = true;
    this.results = [];
    this.stockData = null;
    this.cd.detectChanges();

    this.http.get(`http://localhost:5000/api/${this.query}`).subscribe({
      next: (data: any) => {
        console.log("API response:", data); 
        this.stockData = data;
        this.loading = false;
      },
      error: (err: any) => {
        this.error = "Stock API error";
        this.loading = false;
      }
    });
  }
}