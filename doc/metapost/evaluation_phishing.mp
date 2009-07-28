input metauml;

iActivity.foreColor := (1,1,1);

beginfig(1);
  Begin.b;
  Activity.keyword("Keyword search");
  Activity.picks("Attacker picks person");
  Activity.info("Attacker fetches more", "information about the victim");
  Activity.realname("Acquire real name");
  Activity.address("Acquire e-mail adress");
  Activity.mail("Compose & send", "phishing mail");
  Activity.friends("Keyword search on", "victims friends");
  End.e;

  leftToRight(30)(b, keyword);
  topToBottom(20)(keyword, picks, info, realname, mail, e);
  leftToRight(30)(mail, friends);
  leftToRight(30)(realname, address);

  drawObjects(b, keyword, picks, info, realname, address, mail, friends, e);

  clink(transition)(b, keyword);
  clink(transition)(keyword, picks);
  clink(transition)(picks, info);
  clink(transition)(info, realname);
  clink(transition)(realname, address);
  link(transition)(pathStepY(address.s, mail.n, -10));
  clink(transition)(mail, friends);
  clink(transition)(mail, e);

  link(transition)(pathStepX(friends.e, picks.e, 30));

  %link(transition)(pathStepY(output_data.s, e.n, -10));
  %link(transition)(pathStepY(output_none.s, e.n, -10));

  %link(transition)(pathStepX(missing_args.e, e.e, 100));

  %link(transition)(pathStepX(missing_data.e, output_none.n, 43.5));

  %item(iGuard)("Needed arguments not given")(obj.sw = missing_args.s + (6, 6));
  %item(iGuard)("All needed arguments given")(obj.ne = missing_args.s + (0, -1));

  %item(iGuard)("No data found")(obj.sw = missing_data.s + (6, 6));
  %item(iGuard)("Data found")(obj.se = missing_data.s + (-6, 6));
endfig;

end
