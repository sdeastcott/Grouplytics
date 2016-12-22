import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';

import { AppComponent } from './app.component';
import { LoginComponent } from './login/login.component';
import { ResultPageComponent } from './result-page/result-page.component';
import { GroupListComponent } from './group-list/group-list.component';
import { GroupPanelComponent } from './result-page/group-panel.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    ResultPageComponent,
    GroupListComponent,
    GroupPanelComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
