import { GrouplyticsWebPage } from './app.po';

describe('grouplytics-web App', function() {
  let page: GrouplyticsWebPage;

  beforeEach(() => {
    page = new GrouplyticsWebPage();
  });

  it('should display message saying app works', () => {
    page.navigateTo();
    expect(page.getParagraphText()).toEqual('app works!');
  });
});
