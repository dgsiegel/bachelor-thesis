input metauml;

iState.foreColor := (1,1,1);

beginfig(1);
  Begin.b;
  State.create_twitterapi("Create TwitterAPI Object")();
  State.create_twitterapicall("Create TwitterAPICall Object")();
  State.build("Build URL")();
  State.call("Build Query")();
  State.cache("Check cache")();
  State.rate("Check Rate Limit")();
  State.query("Submit Query")();
  State.cache_store("Cache result")();
  State.return("Return result")();
  ExitPoint.exit;
  End.e;
  End.ethree;

  State.composite("Twitter API Call")(create_twitterapicall, build, call, rate, query, return);
  composite.info.left := composite.info.right := 10;
  composite.info.drawNameLine := 1;

  topToBottom(20)(b, create_twitterapi);
  leftToRight(30)(create_twitterapi, create_twitterapicall);
  topToBottom(20)(create_twitterapicall, build, call, rate, query, return, e);
  leftToRight(70)(call, cache);
  leftToRight(70)(return, cache_store);
  leftToRight(100)(ethree, rate);
  leftToRight(70)(exit, rate);

  drawObject(composite);
  drawObjects(b, create_twitterapi, create_twitterapicall, cache, cache_store, e, ethree, exit);

  clink(transition)(b, create_twitterapi);
  clink(transition)(create_twitterapi, create_twitterapicall);
  clink(transition)(create_twitterapicall, build);
  link(transition)(build.se .. build.se+(10,-7) .. build.ne+(10,7) .. build.ne);
  clink(transition)(build, call);
  clink(transition)(call, cache);
  link(transition)(pathCut(cache, return)(cache.e--cache.e+(10,0)--cache_store.e+(10, -70)--return.w+(-70,-70)--return.w+(-70,0)--return.w));
  link(transition)(pathCut(cache, rate)(cache.s--cache.s+(0,-35)--rate.e));
  clink(transition)(rate, ethree);
  clink(transition)(rate, query);
  link(transition)(pathCut(query, cache_store)(query.e--cache_store.n+(0,35)--cache_store.n));
  clink(transition)(cache_store, return);
  clink(transition)(return, e);

  link(transition)(pathCut(query, exit)(query.w--exit.s+(0,-45)--exit.s));
  clink(transition)(exit, ethree);
  item(iAssoc)("error")(obj.nw = exit.s);
endfig;

end

